# -*- coding: utf-8 -*-
import os
import subprocess
import time
from threading import Event, Thread, Lock
from backend import (Variables, DataBaseMixin, ResultInHtml, CreateDriverMixin)
from backend.events import EventsConnector
import webbrowser
from tkinter_frontend.events import Events, ProgressUpdateEvent
from backend.work_flow import WorkFlow
import queue
from update.update_classs import run_new_app


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
        # канал получения данных из main в поток BackendManager
        self._channel_get: queue.Queue = kwargs.get("channel_get")
        self._lock = Lock()
        self.data = None
        self.__call__()

    def __str__(self):
        return "BackendManager"

    def _show_result(self, var_obj: Variables):
        if not self.check_count_item():
            return
        with self._lock:
            result_html = ResultInHtml(file_name=var_obj.get_filename(), count=self.count_row_in_database())
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
            webbrowser.open(var_obj.get_filename())

    def _receiver_for_main(self):
        from tkinter_frontend.utils import new_flow_btn, update_progress
        """
        Метод получает данные из потока main
        """
        while True:
            data = self._channel_get.get()
            if isinstance(data, Variables):
                print("data from connector: {}".format(data.variables))
                self.data = data
                EventsConnector.variables_put(data.variables)

            elif isinstance(data, ProgressUpdateEvent):
                update_progress(data=(data.text, data.num))

            elif data == Events.push_stop_event:
                print("data from connector: {}".format(data))
                new_flow_btn()
                EventsConnector.push_stop()

            elif data == Events.window_close_event:
                print("data from connector: {}".format(data))
                new_flow_btn()

            elif data == Events.exit_event:
                print("data from connector: {}".format(data))
                if not self.data:
                    # программа завершается корректно только так
                    os._exit(0)
                EventsConnector.push_exit()
                EventsConnector.work_wait()
                # программа завершается корректно только так
                os._exit(0)

            elif data == Events.start_again_event:
                print("data from connector: {}".format(data))
                EventsConnector.variables_put(self.data)

            elif data == Events.exit_after_update_event:
                print("data from connector: {}".format(data))
                if not self.data:
                    run_new_app()
                    os._exit(0)
                else:
                    EventsConnector.push_update()
                    EventsConnector.work_wait()
                    run_new_app()
                    time.sleep(1)
                    os._exit(0)

    def __call__(self, *args, **kwargs):
        receiver_1 = Thread(target=self._receiver_for_main, daemon=True)
        receiver_1.start()
        while True:
            EventsConnector.events_clear()
            print("-" * 10, "waiting for the start", "-" * 10)
            self.create_table()
            try:
                thread = Thread(target=WorkFlow, kwargs={
                    # поток будет отправлять данные в канал
                    "channel_put": self._channel_get,
                })
                thread.start()
                thread.join()
            finally:
                self._show_result(self.data)
                self.delete_database_table()
                self.data = None
                EventsConnector.window_close_wait()
                EventsConnector.work_done()
                print("WorkFlow.__call__() finally")
