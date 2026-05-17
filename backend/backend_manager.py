# -*- coding: utf-8 -*-
import subprocess
from threading import Event, Thread, Lock
from backend import (Variables, DataBaseMixin, ResultInHtml, CreateDriverMixin, create_database)
from backend.events import EventsConnector
import webbrowser
from tkinter_frontend.events import Events, ProgressUpdateEvent
from backend.work_flow import WorkFlow
import queue


def kill_process(pid: str):
    if not isinstance(pid, str):
        pid = str(pid)
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


class BackendManager(DataBaseMixin, CreateDriverMixin):

    def __init__(self, *args, **kwargs):
        # канал получения данных из main в процесс BackendManager
        self._channel_get: queue.Queue = kwargs.get("channel_get")
        self._start = Event()
        self._lock = Lock()
        self.data = {}
        self.__call__()

    def __str__(self):
        return "BackendManager"

    def _show_result(self):
        if not self.check_count_item():
            return
        if not self.data:
            return
        with self._lock:
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
        from tkinter_frontend.utils import new_flow_btn, update_progress
        """
        Метод получает данные из процесса main
        """
        while True:
            data = self._channel_get.get()
            # print("data in BackendManager's _receiver_for_main: {}".format(data))
            if isinstance(data, Variables):
                create_database()
                self.data = data
                self._start.set()
                EventsConnector.variables_put(data.variables)
            elif isinstance(data, ProgressUpdateEvent):
                update_progress(data=(data.text, data.num))
            elif data == Events.push_stop_event:
                print(data)
                new_flow_btn()
                EventsConnector.push_stop()
                self._show_result()
                self.delete_database_table()
                EventsConnector.window_close_wait()
            elif data == Events.exit_event:
                print(data)
                EventsConnector.push_stop()
                self._show_result()
                self.delete_database_table()
                # дождаться закрытия браузера, иначе когда завершается программа, браузер остаётся открытым
                EventsConnector.window_close_wait()
                EventsConnector.destroy_tkinter()
            elif data == Events.window_close_event:
                print(data)
                new_flow_btn()
                self._show_result()
                self.delete_database_table()
                EventsConnector.window_close_wait()
            elif data == Events.start_again_event:
                print(data)
                EventsConnector.window_close_wait()
                self._start.set()
                EventsConnector.variables_put(self.data)
            elif data == Events.exit_after_update_event:
                from main import PROCESS_PID
                print(data)
                self._show_result()
                EventsConnector.push_stop()
                EventsConnector.window_close_wait()
                kill_process(PROCESS_PID)

    def __call__(self, *args, **kwargs):
        receiver_1 = Thread(target=self._receiver_for_main, daemon=True)
        receiver_1.start()
        while True:
            print("-" * 10, "waiting for the start", "-" * 10)
            self._start.wait()
            try:
                # при указании параметра name в Process, процесс BackendManager.__call__() вызывался рекурсивно
                thread = Thread(target=WorkFlow, kwargs={
                    # процесс будет отправлять данные в канал
                    "channel_put": self._channel_get,
                })
                thread.start()
                thread.join()
            finally:
                self._start.clear()
