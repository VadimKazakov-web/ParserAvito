# -*- coding: utf-8 -*-
import multiprocessing
import subprocess
import time
from threading import Event, Thread, Lock
from backend import (Variables, DataBaseMixin, ResultInHtml, CreateDriverMixin)
from backend.events import EventsConnector
import webbrowser
from tkinter_frontend.events import Events, InfoUpdateEvent
from multiprocessing import Process, Queue, JoinableQueue
from backend.work_flow import WorkFlow
import os


def kill_process(pid: str):
    """
    Не используется
    """
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


class BackendManager(DataBaseMixin, CreateDriverMixin):

    def __init__(self, *args, **kwargs):
        # канал получения данных из main в процесс BackendManager
        self._channel_get: multiprocessing.JoinableQueue = kwargs.get("channel_get")
        self._channel_put: multiprocessing.JoinableQueue = kwargs.get("channel_put")
        self._start = Event()
        self._lock = Lock()
        # self._show_result = False
        self.__call__()

    def __str__(self):
        return "BackendManager"

    def _show_result(self):
        self._lock.acquire()
        result_html = ResultInHtml(file_name=self.data.get_filename(), count=self.count_row_in_database())
        result_gen = self.extraction_and_sorting_generator()
        # порядок выдачи отсортированных результатов:
        # по просмотрам за всё время
        data = next(result_gen)
        result_html.write_result(flag="total_views", data=data)
        # по просмотрам сегодня
        data = next(result_gen)
        result_html.write_result(flag="today_views", data=data)
        # по отзывам
        data = next(result_gen)
        result_html.write_result(flag="reviews", data=data)
        # открыть файл с результатами в браузере по умолчанию
        webbrowser.open(self.data.get_filename())
        self._lock.release()

    def _receiver_for_main(self):
        """
        Метод получает данные из процесса main
        """
        while True:
            data = self._channel_get.get()
            # print("data in BackendManager's _receiver_for_main: {}".format(data))
            if isinstance(data, Variables):
                self.data = data
                self._start.set()
            elif data == Events.push_stop_event:
                self._channel_put.put(Events.new_flow_event)
                EventsConnector.push_stop()
            elif data == Events.exit_event:
                EventsConnector.push_stop()

    def _receiver_for_workflow(self):
        """
        Метод получает данные из процесса WorkFlow
        """
        while True:
            EventsConnector.window_close_event.clear()
            data = self._channel_workflow_get.get()
            # print("data in BackendManager's _receiver_for_workflow: {}".format(data))
            if isinstance(data, InfoUpdateEvent):
                self._channel_put.put(data)
            elif data == Events.window_close_event:
                self._show_result()
                self._channel_put.put(Events.new_flow_event)
                EventsConnector.window_close()
                return

    def __call__(self, *args, **kwargs):
        receiver_1 = Thread(target=self._receiver_for_main, daemon=True)
        receiver_1.start()
        while True:
            print("-" * 10, "waiting for the start", "-" * 10)
            self._start.wait()
            try:
                # после завершения процесса WorkFlow, нужно передавать новый объект Queue
                # канал получения данных из процесса WorkFlow процесс BackendManager
                self._channel_workflow_get = Queue(maxsize=20)
                # канал передачи данных из процесса BackendManager в дочерний процесс WorkFlow
                self._channel_workflow_put = JoinableQueue(maxsize=20)
                receiver_2 = Thread(target=self._receiver_for_workflow)
                receiver_2.start()
                # при указании параметра name в Process, процесс BackendManager.__call__() вызывался рекурсивно
                thread = Thread(target=WorkFlow, kwargs={
                    # процесс будет получать данные с канала
                    "channel_get": self._channel_workflow_put,
                    # процесс будет отправлять данные в канал
                    "channel_put": self._channel_workflow_get,
                })
                thread.start()
                time.sleep(1)
                self._channel_workflow_put.put(self.data)
                thread.join()
                print("proc.join() done")
                receiver_2.join()
                print("receiver_2.join() done")
            finally:
                self._start.clear()
