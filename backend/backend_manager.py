# -*- coding: utf-8 -*-
import os
import subprocess
import time
from threading import Thread
from backend import (Variables, DataBaseMixin, CreateDriverMixin)
from backend.events import EventsConnector
from tkinter_frontend.events import Events, ProgressUpdateEvent
from backend.work_flow import WorkFlow
import queue
from update.update_classs import run_new_app


def kill_process(pid: str) -> None:
    pid = str(pid)
    complete_process = subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, shell=True)
    if complete_process.returncode == 0:
        print(complete_process.stdout.decode(encoding='oem'))
    else:
        print(complete_process.stderr.decode(encoding='oem'))


class BackendManager(DataBaseMixin, CreateDriverMixin):

    def __init__(self, *args, **kwargs):
        # канал получения данных из tkinter в поток BackendManager
        self._channel_get: queue.Queue = kwargs.get("channel_get")
        self.data = None

    def __str__(self) -> str:
        return "BackendManager"

    def _receiver_for_main(self) -> None:
        from tkinter_frontend.utils import new_flow_btn, update_progress
        """
        Метод получает данные из потока main
        """
        while True:
            data = self._channel_get.get()
            if isinstance(data, Variables):
                print("data from connector: {}".format(data.variables))
                self.data = data
                EventsConnector.variables_put(data)

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
                if self.data:
                    EventsConnector.push_exit()
                    EventsConnector.work_wait()
                # программа завершается корректно только так
                os._exit(0)

            elif data == Events.start_again_event:
                print("data from connector: {}".format(data))
                EventsConnector.variables_put(self.data)

            elif data == Events.exit_after_update_event:
                print("data from connector: {}".format(data))
                if self.data:
                    EventsConnector.push_update()
                    EventsConnector.work_wait()
                run_new_app()
                time.sleep(1)
                os._exit(0)

    def __call__(self, *args, **kwargs) -> None:
        receiver_1 = Thread(target=self._receiver_for_main, daemon=True)
        receiver_1.start()
        while True:
            print("-" * 10, "waiting for the start", "-" * 10)
            with WorkFlow(channel_put=self._channel_get) as work_flow:
                work_flow()
