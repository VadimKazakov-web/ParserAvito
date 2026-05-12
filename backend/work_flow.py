# -*- coding: utf-8 -*-
import queue
import re
import threading
import time
from threading import Thread
from backend import CreateDriverMixin, DataBaseMixin, \
    SearchLinks, CollectData
from backend.interceptor_headers import InterceptorHeaders
from backend.open_url import OpenUrl
from backend.open_advertisement import OpenAdvertisement
from backend.utils import CreatingLinks
from backend.utils.scroll_page import scroll_page
from tkinter_frontend.events import Events, InfoUpdateEvent
from backend.variables import Variables
from backend.utils.timeout import TimeoutMixin
import multiprocessing
from seleniumwire.webdriver import Chrome


def rewind_gen(num, gen):
    while num != 0:
        next(gen)
        num -= 1
    return gen


class WorkFlow(CreateDriverMixin, DataBaseMixin):
    var = None

    def __init__(self, *args, **kwargs):
        self._channel_get: multiprocessing.Queue = kwargs.get("channel_get")
        self._channel_put: multiprocessing.Queue = kwargs.get("channel_put")
        self._open_pages_global_counter = 0
        self._open_advertisement_global_counter = 0
        self.driver: Chrome = self.create_driver()
        self.driver.request_interceptor = InterceptorHeaders.request_interceptor
        self.driver.response_interceptor = InterceptorHeaders.response_interceptor
        self._start = threading.Event()
        self.data = None
        self._continue = "continue"
        try:
            self.__call__()
        except Exception as err:
            if re.search(r"no such window|session deleted|cannot determine loading status", str(err)):
                pass
            else:
                print(err)
        finally:
            self.driver.quit()
            self._channel_put.put(Events.window_close_event)
            print("after WorkFlow's self.__call__()")

    def __str__(self):
        return "WorkFlow"

    def _receiver(self):
        while True:
            data = self._channel_get.get()
            # print("data in WorkFlow's _receiver: {}".format(data))
            if isinstance(data, Variables):
                self.data = data.variables
                self._start.set()
            elif data == Events.push_stop_event:
                self.driver.quit()
                self._channel_put.put(Events.new_flow_event)
                # экспериментальный, более низкоуровневый способ закрытия окна браузера
                # remote_server_addr = self.driver.command_executor._client_config.remote_server_addr
                # url = "{}/session/{}/window".format(remote_server_addr, self.driver.session_id)
                # response = requests.delete(url)

    def __call__(self, *args, **kwargs):
        receiver = Thread(target=self._receiver, daemon=True)
        receiver.start()
        self._start.wait()
        self._work_flow(*args, **kwargs)

    def _work_flow(self, pages=0, advertisement=0):
        # создание ссылок на страницы
        creating_links_gen = CreatingLinks(url=self.data.get("url"), pages=self.data.get("pages"))
        # перемотка вперёд, если нужно
        creating_links_gen = rewind_gen(pages, creating_links_gen())
        # переход на каждую страницу
        for url_page in creating_links_gen:
            flag_page = self._open_page_script(url_page)
            if flag_page == self._continue:
                continue
            # установка заголовка "referer"
            InterceptorHeaders.referer = url_page
            # поиск ссылок на каждое объявление
            search_links_gen = SearchLinks(self.driver)
            # перемотка вперёд, если нужно
            search_links_gen = rewind_gen(advertisement, search_links_gen())
            # переход на каждое объявление
            for url_advertisement in search_links_gen:
                flag_adv = self._open_adv_script(url_advertisement)
                if flag_adv == self._continue:
                    continue
                print("\ntitle: {}".format(self.driver.title))
                self._connection_failure_script()
                # прокрутка страницы
                scroll_page(driver=self.driver, height=1200)
                # сбор данных из объявления
                collect_data = CollectData(self.driver)
                result = collect_data()
                print("data adv: {}\n".format(result))
                # внесение объявления в базу данных
                self.insert_in_database(result)
                # закрыть вкладку
                self.driver.close()
                # вернуться на вкладку страницы
                self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(0.5)
                # прокрутка страницы
                scroll_page(driver=self.driver, height=340)
                self._open_advertisement_global_counter += 1
            self._open_pages_global_counter += 1

    def _connection_failure_script(self):
        if self.driver.title == "www.avito.ru":
            print("connection failure, restart...")
            # добавить в диапазон таймаута по одной секунде в начало и в конец
            TimeoutMixin.timeout_add_one()
            # закрыть окно браузера
            self.driver.quit()
            # создать новое окно браузера
            self.driver = self.create_driver()
            self._work_flow(pages=self._open_pages_global_counter,
                            advertisement=self._open_advertisement_global_counter)
            return

    def _update_title(self, driver):
        # задержка для получения актуального заголовка страницы
        time.sleep(2)
        info_upd = InfoUpdateEvent(driver.title)
        self._channel_put.put(info_upd)

    def _open_page_script(self, url_page):
        print("current page: {}".format(self._open_pages_global_counter + 1))
        open_url = OpenUrl(driver=self.driver, url=url_page, update_title_callback=self._update_title)
        if not open_url():
            return self._continue

    def _open_adv_script(self, url_advertisement):
        # открытие ссылки в новой вкладке
        open_adv = OpenAdvertisement(driver=self.driver, url=url_advertisement,
                                     update_title_callback=self._update_title)
        if not open_adv():
            self.driver.switch_to.window(self.driver.window_handles[0])
            return self._continue
