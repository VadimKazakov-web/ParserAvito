# -*- coding: utf-8 -*-
import asyncio
import os
import queue
import shutil
import time
from backend import Variables
from settings import APP_TEMPORARY
from tkinter_frontend.events import Events
from tkinter_frontend.utils import update_info
from update.utills.utills import run_new_app
from backend.data_queue import connector


async def recv(self) -> None:
    from tkinter_frontend.utils import new_flow_btn
    """
    Метод получает данные из потока main
    """
    while True:
        try:
            data = connector.get(block=False)
        except queue.Empty:
            await asyncio.sleep(1)
        else:
            if isinstance(data, Variables):
                """
                Получение ссылки, названия файла и кол-во страниц для сканирования из интерфейса tkinter
                """
                print("data from connector: {}".format(data.variables))
                self.data = data
                self._start.set()

            elif data == Events.push_stop_event:
                """
                Нажатие кнопки "stop"
                """
                print("data from connector: {}".format(data))
                new_flow_btn()
                self.stop = True
                self.work_task.cancel()
                return

            elif data == Events.window_close_event:
                """
                Закрытие окна браузера
                """
                print("data from connector: {}".format(data))
                new_flow_btn()

            elif data == Events.exit_event:
                """
                Закрытие главного окна программы
                """
                update_info("Ожидайте завершения программы.")
                print("data from connector: {}".format(data))
                if self._start.is_set():
                    self.stop = True
                    self.work_task.cancel()
                    await self._work.wait()
                else:
                    self.driver.quit()
                try:
                    shutil.rmtree(APP_TEMPORARY)
                except FileNotFoundError:
                    pass
                time.sleep(0.5)
                os._exit(0)

            elif data == Events.exit_after_update_event:
                """
                Действия, которые происходят после обновления программы: запуск новой программы
                с помощью утилиты windows schtasks /run, и закрытия старой программы
                """
                print("data from connector: {}".format(data))
                if self.data:
                    self.stop = True
                    self._work.wait()
                run_new_app()
                time.sleep(1)
                os._exit(0)

        await asyncio.sleep(0)
