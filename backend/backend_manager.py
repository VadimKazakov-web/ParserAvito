# -*- coding: utf-8 -*-
import multiprocessing
import subprocess
import time
from threading import Event, Thread
from backend import (Variables, DataBaseMixin, ResultInHtml, CreateDriverMixin)
import webbrowser
from tkinter_frontend.events import Events, InfoUpdateEvent
from multiprocessing import Process, Queue
from backend.work_flow import WorkFlow
import os


def kill_process(pid: str):
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


class BackendManager(DataBaseMixin, CreateDriverMixin):

    def __init__(self, *args, **kwargs):
        # self._channel_get_for_work_flow = Queue(maxsize=20)

        # канал получения данных из main в процесс BackendManager
        self._channel_get: multiprocessing.Queue = kwargs.get("channel_get")
        self._channel_put: multiprocessing.Queue = kwargs.get("channel_put")
        self._start = Event()
        self._pid_work_flow = None
        self.__call__()

    def __str__(self):
        return "BackendManager"

    def _show_result(self):
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

    def _receiver_for_main(self):
        while True:
            data = self._channel_get.get()
            print("data in BackendManager's _receiver_for_main: {}".format(data))
            if isinstance(data, Variables):
                self.data = data
                self._start.set()
            elif data == Events.push_stop_event:
                self._channel_get_for_work_flow.put(Events.push_stop_event)
                self._show_result()
                time.sleep(2)
                kill_process(self._pid_work_flow)

    def _receiver_for_workflow(self):
        while True:
            try:
                data = self._channel_put_for_work_flow.get()
                print("data in BackendManager's _receiver_for_workflow: {}".format(data))
            except AttributeError:
                time.sleep(2)
            else:
                if isinstance(data, InfoUpdateEvent):
                    self._channel_put.put(data)
                elif data == Events.new_flow_event:
                    self._channel_put.put(Events.new_flow_event)
                    time.sleep(2)
                    kill_process(self._pid_work_flow)

    def __call__(self, *args, **kwargs):
        print("pid BackendManager proc: {}".format(os.getpid()))
        receiver_1 = Thread(target=self._receiver_for_main, daemon=True)
        receiver_1.start()
        receiver_2 = Thread(target=self._receiver_for_workflow, daemon=True)
        receiver_2.start()
        while True:
            print("-" * 10, "waiting for the start", "-" * 10)
            self._start.wait()
            try:
                # канал передачи данных из процесса BackendManager в дочерний процесс WorkFlow,
                # после завершения процесса WorkFlow, нужно передавать новый объект Queue
                self._channel_get_for_work_flow = Queue(maxsize=20)
                # канал получения данных из процесса WorkFlow процесс BackendManager
                self._channel_put_for_work_flow = Queue(maxsize=20)
                # при указании параметра name в Process, процесс BackendManager.__call__() вызывался рекурсивно
                proc = Process(target=WorkFlow, kwargs={
                    # процесс будет получать данные с канала
                    "channel_get": self._channel_get_for_work_flow,
                    # процесс будет отправлять данные в канал
                    "channel_put": self._channel_put_for_work_flow,
                })
                proc.start()
                self._pid_work_flow = str(proc.ident)
                print("pid work_flow proc: {}".format(self._pid_work_flow))
                time.sleep(1)
                self._channel_get_for_work_flow.put(self.data)
                proc.join()
            finally:
                self._start.clear()
                print("+ put data in main's _receiver in BackendManager.__call__()")
                self._channel_put.put(Events.new_flow_event)
