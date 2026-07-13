# -*- coding: utf-8 -*-
import logging
import queue
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
import selenium.common


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

    async def _check_flags(self):
        while True:
            if self.stop:
                self.work_task.cancel()
                return
            if self.connection_failure:
                return
            await asyncio.sleep(0)

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

        logging.warning("error type: {}".format(exc_type))
        if (exc_type == selenium.common.exceptions.NoSuchWindowException
                or exc_type == selenium.common.exceptions.InvalidSessionIdException):
            self._channel_put.put(Events.window_close_event)
        elif exc_type == selenium.common.exceptions.NoSuchElementException:
            update_info("необходимые данные на странице не найдены")
            raise
        elif exc_type:
            raise

    def _driver_init(self, read_cookie=True):
        self.driver: Chrome = self.create_driver()
        # self.interceptor_headers = InterceptorHeaders(read_cookie)
        # self.driver.request_interceptor = self.interceptor_headers.request_interceptor
        # self.driver.response_interceptor = self.interceptor_headers.response_interceptor

    def __str__(self):
        return "WorkFlow"

    async def __call__(self, *args, **kwargs):
        while True:
            self.connection_failure = False
            # проверка, не произошли ли события нажатия на кнопки stop, exit и т.д...
            self._tasks.append(asyncio.create_task(self._check_flags()))
            # актуализация прогресса
            self._tasks.append(asyncio.create_task(self._update_progress()))
            # главная задача
            self.work_task = asyncio.create_task(self._work_flow(pages=self._open_pages_global_counter,
                                                                 advertisement=self._open_advertisement_in_page))
            self._tasks.append(self.work_task)
            for task in self._tasks:
                task.add_done_callback(self._tasks.remove)
            try:
                result = await self.work_task
            except asyncio.CancelledError:
                self.driver.quit()
                return
            except (selenium.common.exceptions.InvalidSessionIdException,
                    selenium.common.exceptions.NoSuchWindowException):
                self._channel_put.put(Events.window_close_event)
                for task in self._tasks:
                    task.cancel()
                return
            else:
                self.driver.quit()
                self._driver_init(read_cookie=False)

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
                await asyncio.sleep(0)
                # проверка на обрыв соединения
                if self._connection_failure_script():
                    self.connection_failure = True
                    return
                # прокрутка страницы
                await scroll_page(driver=self.driver, height=1200)
                # сбор данных из объявления
                collect_data = CollectData(self.driver)
                result = collect_data()
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
        """
        Проверка, не произошёл ли обрыв соединения
        """
        # if self._open_advertisement_global_counter == 2:
        #     logging.warning("connection failure, restart...(TEST!)")
        #     return True
        if self.driver.title == "www.avito.ru":
            logging.warning("connection failure, restart...")
            return True

    async def _update_progress(self):
        while not self.stop and not self.connection_failure:
            progr_upd = ProgressData(self.driver.title, self._open_advertisement_global_counter)
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
