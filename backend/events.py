# -*- coding: utf-8 -*-
import threading
import time

from exceptions import PushStopButton, PushExit, PushUpdate


class MutexVar:

    def __init__(self, var):
        self._lock = threading.Lock()
        self._var = var

    def get(self):
        with self._lock:
            return self._var

    def set(self, var):
        with self._lock:
            self._var = var


class EventsConnector:
    _push_stop_event = threading.Event()
    _push_exit_event = threading.Event()
    _push_update_event = threading.Event()
    _window_close_event = threading.Event()
    _destroy_tkinter_event = threading.Event()
    _work_done_event = threading.Event()
    _var_event = threading.Event()
    var = MutexVar(None)

    @classmethod
    def push_stop(cls):
        cls._push_stop_event.set()

    @classmethod
    def push_update(cls):
        cls._push_update_event.set()

    @classmethod
    def push_exit(cls):
        cls._push_exit_event.set()

    @classmethod
    def events_handler(cls):
        if cls._push_stop_event.is_set():
            cls._push_stop_event.clear()
            raise PushStopButton
        elif cls._push_exit_event.is_set():
            cls._push_exit_event.clear()
            raise PushExit
        elif cls._push_update_event.is_set():
            cls._push_update_event.clear()
            raise PushUpdate

    @classmethod
    def destroy_tkinter(cls):
        cls._destroy_tkinter_event.set()

    @classmethod
    def destroy_tkinter_wait(cls):
        while True:
            # Чтобы не блокировать главный процесс
            if cls._destroy_tkinter_event.is_set():
                cls._destroy_tkinter_event.clear()
                return
            # time.sleep(1)

    @classmethod
    def window_close(cls):
        cls._window_close_event.set()

    @classmethod
    def window_close_wait(cls):
        cls._window_close_event.wait()

    @classmethod
    def work_done(cls):
        cls._work_done_event.set()

    @classmethod
    def work_unset(cls):
        cls._work_done_event.clear()

    @classmethod
    def work_wait(cls):
        cls._work_done_event.wait()

    @classmethod
    def variables_put(cls, data):
        cls.var.set(data)
        cls._var_event.set()

    @classmethod
    def variables_wait(cls):
        cls._var_event.wait()
        cls._var_event.clear()
        return cls.var.get()

