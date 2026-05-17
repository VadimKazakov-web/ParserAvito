# -*- coding: utf-8 -*-
import threading
from exceptions import PushStopButton


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
    push_stop_event = threading.Event()
    window_close_event = threading.Event()
    destroy_tkinter_event = threading.Event()
    var_event = threading.Event()
    var = MutexVar(None)

    @classmethod
    def push_stop(cls):
        cls.push_stop_event.set()

    @classmethod
    def events_handler(cls):
        if cls.push_stop_event.is_set():
            cls.push_stop_event.clear()
            raise PushStopButton
        elif cls.window_close_event.is_set():
            pass

    @classmethod
    def destroy_tkinter(cls):
        cls.destroy_tkinter_event.set()

    @classmethod
    def destroy_tkinter_wait(cls):
        cls.destroy_tkinter_event.wait(timeout=4)
        cls.destroy_tkinter_event.clear()

    @classmethod
    def window_close(cls):
        cls.window_close_event.set()

    @classmethod
    def window_close_wait(cls):
        cls.window_close_event.wait(timeout=4)
        cls.window_close_event.clear()

    @classmethod
    def variables_wait(cls):
        cls.var_event.wait()
        cls.var_event.clear()
        return cls.var.get()

    @classmethod
    def variables_put(cls, data):
        cls.var.set(data)
        cls.var_event.set()



