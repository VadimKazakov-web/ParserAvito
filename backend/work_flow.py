# -*- coding: utf-8 -*-
import logging
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
from seleniumwire.webdriver import Chrome
from tkinter_frontend.utils import update_info
import asyncio


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

    CONTINUE = "continue"
    DONE = "done"

    def __init__(self, *args, **kwargs):
        self._channel_put: queue.Queue = kwargs.get("channel_put")
        self._open_pages_global_counter = 0
        self._open_advertisement_global_counter = 0
        self._open_advertisement_in_page = 0
        self._start = threading.Event()
        self.data: Variables = kwargs.get("data")
        self._tasks = []
        self.stop = False
        self.connection_failure = False

    async def _check_flags(self):
        while True:
            if self.stop:
                self._tasks_cancel()
                self.driver.quit()
            await asyncio.sleep(0)

    def _tasks_cancel(self):
        if self._tasks:
            for task in self._tasks:
                task.cancel()
                self._tasks.remove(task)

    def __enter__(self):
        EventsConnector.work_unset()
        self.create_table()
        update_info("загрузка и запуск chromedriver")
        self._driver_init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.data:
            self._show_result(self.data)
        self.delete_database_table()
        EventsConnector.work_done()

    def _driver_init(self, read_cookie=True):
        self.driver: Chrome = self.create_driver()
        self.interceptor_headers = InterceptorHeaders(read_cookie)
        self.driver.request_interceptor = self.interceptor_headers.request_interceptor
        self.driver.response_interceptor = self.interceptor_headers.response_interceptor

    def __str__(self):
        return "WorkFlow"

    async def __call__(self, *args, **kwargs):
        try:
            await self._start_coro(*args, **kwargs)
        except Exception as err:
            err_info = str(err)[0:130]
            logging.warning(err_info)
            if re.search(r'no such window|session deleted|cannot determine loading status', err_info):
                self._channel_put.put(Events.window_close_event)
                self.driver.quit()
                return
            elif re.search(r'unknown error: net::ERR_CONNECTION_CLOSED', err_info):
                self.driver.quit()
                self._driver_init(read_cookie=False)
                time.sleep(1)
            elif re.search(r'no such element', err_info):
                update_info("необходимые данные на странице не найдены")
                raise
            else:
                raise

    async def _start_coro(self, *args, **kwargs):
        while True:
            self.connection_failure = False
            # проверка, не произошли ли события нажатия на кнопки stop, exit и т.д...
            self._tasks.append(asyncio.create_task(self._check_flags()))
            # актуализация прогресса
            self._tasks.append(asyncio.create_task(self._update_progress(self.driver)))
            work_task = asyncio.create_task(self._work_flow(pages=self._open_pages_global_counter,
                                                            advertisement=self._open_advertisement_in_page))
            work_task.add_done_callback(self._tasks.remove)
            self._tasks.append(work_task)
            try:
                result = await work_task
            except asyncio.CancelledError:
                return
            finally:
                self._tasks_cancel()

    async def _work_flow(self, pages=0, advertisement=0):
        # создание ссылок на страницы
        creating_links_gen = CreatingLinks(url=self.data.get_url(), pages=self.data.get_pages())
        # перемотка вперёд, если нужно
        creating_links_gen = rewind_gen(pages, creating_links_gen())
        # переход на каждую страницу
        for url_page in creating_links_gen:
            update_info("переход по web страницам")
            logging.warning("current page: {}".format(self._open_pages_global_counter + 1))
            flag_page = await self._open_page_script(url_page)
            if flag_page == self.CONTINUE:
                continue
            await asyncio.sleep(0)
            # установка заголовка "referer"
            InterceptorHeaders.referer = url_page
            # поиск ссылок на каждое объявление
            search_links_gen = SearchLinks(self.driver)
            # перемотка вперёд, если нужно
            search_links_gen = rewind_gen(advertisement, search_links_gen())
            # переход на каждое объявление
            for url_advertisement in search_links_gen:
                flag_adv = await self._open_adv_script(url_advertisement)
                if flag_adv == self.CONTINUE:
                    continue
                # проверка на обрыв соединения
                if self._connection_failure_script():
                    return
                await asyncio.sleep(0)
                # прокрутка страницы
                await scroll_page(driver=self.driver, height=1200)
                # сбор данных из объявления
                collect_data = CollectData(self.driver)
                result = collect_data()
                # print("data adv: {}\n".format(result))
                # внесение объявления в базу данных
                self.insert_in_database(result)
                self._open_advertisement_global_counter += 1
                self._open_advertisement_in_page += 1
                await asyncio.sleep(0)
                # закрыть вкладку
                self.driver.close()
                # вернуться на вкладку страницы
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(0.5)
                # прокрутка страницы
                await scroll_page(driver=self.driver, height=340)
            self._open_pages_global_counter += 1
            self._open_advertisement_in_page = 0
        return self.DONE

    def _connection_failure_script(self):
        # if self._open_advertisement_global_counter == 1:
        #     logging.warning("connection failure, restart...(TEST!)")
        #     self.connection_failure = True
        #     # закрыть окно браузера
        #     self.driver.quit()
        #     self._driver_init(read_cookie=False)
        #     return True
        """
        Проверка, не произошёл ли обрыв соединения
        """
        if self.driver.title == "www.avito.ru":
            logging.warning("connection failure, restart...")
            # закрыть окно браузера
            self.driver.quit()
            self._driver_init(read_cookie=False)
            return True

    async def _update_progress(self, driver):
        while not self.stop and not self.connection_failure:
            progr_upd = ProgressData(driver.title, self._open_advertisement_global_counter)
            self._channel_put.put(progr_upd)
            await asyncio.sleep(0)

    async def _open_page_script(self, url_page):
        # открытие страницы
        open_url = OpenUrl(driver=self.driver, url=url_page)
        result = await open_url()
        return result

    async def _open_adv_script(self, url_advertisement):
        # открытие ссылки в новой вкладке
        open_adv = OpenAdvertisement(driver=self.driver, url=url_advertisement)
        result = await open_adv()
        if result == OpenAdvertisement.PAGE_NOT_FOUND:
            self.driver.switch_to.window(self.driver.window_handles[0])
            return self.CONTINUE

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
