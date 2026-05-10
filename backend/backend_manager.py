# -*- coding: utf-8 -*-
import subprocess
import time
from threading import Event, Thread
from backend import (Variables, DataBaseMixin, ResultInHtml, CreateDriverMixin)
import webbrowser
from tkinter_frontend.events import Events
from multiprocessing import Process, Queue
from backend.work_flow import WorkFlow
import os


def kill_work_flow(pid):
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


class BackendManager(DataBaseMixin, CreateDriverMixin):

    def __init__(self, ):
        # канал передачи данных из процесса BackendManager в дочерний процесс WorkFlow
        self._channel_work_flow = Queue()
        self._pid_work_flow = None

    def _show_result(self):
        result_html = ResultInHtml(file_name=Variables.get_filename(), count=self.count_row_in_database())
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
        webbrowser.open(Variables.get_filename())

    def _receiver(self):
        while True:
            data = self._channel.get()
            print("data in _receiver BackendManager: {}".format(data))
            if isinstance(data, dict):
                if Variables.set_var(data):
                    self._start.set()
            elif data == Events.push_stop_event:
                self._channel_work_flow.put(Events.push_stop_event)
                self._start.clear()
                self._show_result()
                time.sleep(4)
                kill_work_flow(self._pid_work_flow)

    def __call__(self, *args, **kwargs):
        print("pid BackendManager proc: {}".format(os.getpid()))
        # канал получения данных из tkinter в процесс BackendManager
        self._channel = kwargs.get("channel")
        # канал передачи данных из процесса BackendManager в главный процесс
        self._channel_for_main_proc = kwargs.get("channel_for_main_proc")
        self._start = Event()
        while True:
            receiver = Thread(target=self._receiver, daemon=True)
            receiver.start()
            time.sleep(0.1)
            print("-" * 10, "waiting for the start", "-" * 10)
            self._start.wait()
            try:
                proc = Process(target=WorkFlow, kwargs={
                    "channel": self._channel_work_flow,
                    "channel_for_main_proc": self._channel_for_main_proc,
                })
                proc.start()
                self._pid_work_flow = str(proc.ident)
                print("pid work_flow proc: {}".format(self._pid_work_flow))
                self._channel_work_flow.put(Variables())
                proc.join()
            finally:
                self._start.clear()
                self._channel_for_main_proc.put(Events.new_flow_event)
