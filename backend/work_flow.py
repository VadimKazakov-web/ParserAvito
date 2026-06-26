# -*- coding: utf-8 -*-
import queue
import re
import threading
import time
import webbrowser
from backend import CreateDriverMixin, DataBaseMixin, \
    SearchLinks, ResultInHtmlMixin, Variables
from backend.collect_data import CollectData
from backend.interceptor_headers import InterceptorHeaders
from backend.open_url import OpenUrl
from backend.open_advertisement import OpenAdvertisement
from backend.utils import CreatingLinks
from backend.utils.scroll_page import scroll_page
from backend.events import EventsConnector
from tkinter_frontend.events import Events, ProgressData
from backend.utils.timeout import TimeoutMixin
from seleniumwire.webdriver import Chrome
from exceptions import PushStopButton, PushExit, PushUpdate


# экспериментальный, более низкоуровневый способ закрытия окна браузера
# remote_server_addr = self.driver.command_executor._client_config.remote_server_addr
# url = "{}/session/{}/window".format(remote_server_addr, self.driver.session_id)
# response = requests.delete(url)

def rewind_gen(num, gen):
    while num != 0:
        next(gen)
        num -= 1
    return gen


class WorkFlow(CreateDriverMixin, DataBaseMixin, ResultInHtmlMixin):

    """
    Класс реализует основную логику работы программы
    """

    def __init__(self, *args, **kwargs):
        self._channel_put: queue.Queue = kwargs.get("channel_put")
        self._open_pages_global_counter = 0
        self._open_advertisement_global_counter = 0
        self._open_advertisement_in_page = 0
        self._start = threading.Event()
        self.data: Variables = kwargs.get("data")
        self._continue = "continue"
        self._connection_failure = "connection failure"

    def __enter__(self):
        EventsConnector.work_unset()
        self.create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.data:
            self._show_result(self.data)
        self.delete_database_table()
        EventsConnector.work_done()

    def _driver_init(self):
        self.driver: Chrome = self.create_driver()
        self.interceptor_headers = InterceptorHeaders()
        self.driver.request_interceptor = self.interceptor_headers.request_interceptor
        self.driver.response_interceptor = self.interceptor_headers.response_interceptor

    def __str__(self):
        return "WorkFlow"

    def __call__(self, *args, **kwargs):
        while True:
            self._driver_init()
            try:
                self._start_gen(*args, **kwargs)
            except (PushStopButton, PushUpdate, PushExit) as err:
                print(err)
                self.interceptor_headers.write_cookie()
                self.driver.quit()
                return
            except Exception as err:
                err_info = str(err)[0:130]
                print(err_info)
                if re.search(r'no such window|session deleted|cannot determine loading status', err_info):
                    self._channel_put.put(Events.window_close_event)
                    self.interceptor_headers.write_cookie()
                    self.driver.quit()
                    return
                elif re.search(r'unknown error: net::ERR_CONNECTION_CLOSED', err_info):
                    self.driver.quit()
                    self.interceptor_headers.cookie_dict = {}
                    print("90% of the problem is incorrect cookies")
                    time.sleep(3)
                else:
                    raise

    def _start_gen(self, *args, **kwargs):
        while True:
            for step in self._work_flow(pages=self._open_pages_global_counter,
                                        advertisement=self._open_advertisement_in_page):
                # если произошёл обрыв соединения, прекращается текущий проход по генератору,
                # закрывается окно браузера и создаётся новое, генератор перематывается вперёд на
                # нужное кол-во страниц и объявлений
                if step == self._connection_failure:
                    break
                # проверка, не произошли ли события нажатия на кнопки stop, exit и т.д...
                EventsConnector.events_handler()
                # актуализация прогресса
                self._update_progress(self.driver)
            else:
                return

    def _work_flow(self, pages=0, advertisement=0):
        # создание ссылок на страницы
        creating_links_gen = CreatingLinks(url=self.data.get_url(), pages=self.data.get_pages())
        # перемотка вперёд, если нужно
        creating_links_gen = rewind_gen(pages, creating_links_gen())
        # переход на каждую страницу
        for url_page in creating_links_gen:
            flag_page = yield from self._open_page_script(url_page)
            if flag_page == self._continue:
                continue
            yield
            # установка заголовка "referer"
            InterceptorHeaders.referer = url_page
            # поиск ссылок на каждое объявление
            search_links_gen = SearchLinks(self.driver)
            # перемотка вперёд, если нужно
            search_links_gen = rewind_gen(advertisement, search_links_gen())
            # переход на каждое объявление
            for url_advertisement in search_links_gen:
                flag_adv = yield from self._open_adv_script(url_advertisement)
                if flag_adv == self._continue:
                    continue
                # print("\ntitle: {}".format(self.driver.title))
                # проверка на обрыв соединения
                flag_conn = yield from self._connection_failure_script()
                if flag_conn:
                    yield flag_conn
                yield
                # прокрутка страницы
                yield from scroll_page(driver=self.driver, height=1200)
                # сбор данных из объявления
                collect_data = CollectData(self.driver)
                result = collect_data()
                # print("data adv: {}\n".format(result))
                # внесение объявления в базу данных
                self.insert_in_database(result)
                self._open_advertisement_global_counter += 1
                self._open_advertisement_in_page += 1
                yield
                # закрыть вкладку
                self.driver.close()
                # вернуться на вкладку страницы
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(0.5)
                # прокрутка страницы
                yield from scroll_page(driver=self.driver, height=340)
            self._open_pages_global_counter += 1
            self._open_advertisement_in_page = 0

    def _connection_failure_script(self):
        """
        Проверка, не произошёл ли обрыв соединения
        """
        if self.driver.title == "www.avito.ru":
            print("connection failure, restart...")
            # добавить в диапазон таймаута по одной секунде в начало и в конец
            TimeoutMixin.timeout_add_one()
            # закрыть окно браузера
            self.driver.quit()
            # создать новое окно браузера
            self.driver = self.create_driver()
            yield self._connection_failure

    def _update_progress(self, driver):
        progr_upd = ProgressData(driver.title, self._open_advertisement_global_counter)
        self._channel_put.put(progr_upd)

    def _open_page_script(self, url_page):
        print("current page: {}".format(self._open_pages_global_counter + 1))
        open_url = OpenUrl(driver=self.driver, url=url_page)
        result = yield from open_url()
        return result

    def _open_adv_script(self, url_advertisement):
        # открытие ссылки в новой вкладке
        open_adv = OpenAdvertisement(driver=self.driver, url=url_advertisement)
        result = yield from open_adv()
        if result == OpenAdvertisement.page_not_found:
            self.driver.switch_to.window(self.driver.window_handles[0])
            return self._continue

    def _show_result(self, var_obj: Variables) -> None:
        """
        Получение объявлений из базы данных, запись в html файл, открытие файла в браузере по умолчанию
        """
        if not self.check_count_item():
            return
        self.create_result_file(file_name=var_obj.get_filename(), count=self.count_row_in_database())
        result_gen = self.extraction_and_sorting_generator()
        # порядок выдачи отсортированных результатов:
        # по просмотрам за всё время
        data = next(result_gen)
        self.write_result(flag="total_views", data=data)
        # по просмотрам сегодня
        data = next(result_gen)
        self.write_result(flag="today_views", data=data)
        # по отзывам
        data = next(result_gen)
        self.write_result(flag="reviews", data=data)
        # открыть файл с результатами в браузере по умолчанию
        webbrowser.open(var_obj.get_filename())
