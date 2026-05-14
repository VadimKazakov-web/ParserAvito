# -*- coding: utf-8 -*-
import threading
from exceptions import PushStopButton


class EventsConnector:
    push_stop_event = threading.Event()
    window_close_event = threading.Event()
    destroy_tkinter_event = threading.Event()
    var_event = threading.Event()
    var = None

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
        cls.destroy_tkinter_event.wait(timeout=10)
        if cls.destroy_tkinter_event.is_set():
            cls.destroy_tkinter_event.clear()
            return True
        else:
            return False

    @classmethod
    def window_close(cls):
        cls.window_close_event.set()

    @classmethod
    def window_close_wait(cls):
        cls.window_close_event.wait(timeout=3)
        if cls.window_close_event.is_set():
            cls.window_close_event.clear()
            return True
        else:
            return False

    @classmethod
    def variables_wait(cls):
        cls.var_event.wait()
        cls.var_event.clear()
        return cls.var

    @classmethod
    def variables_put(cls, data):
        cls.var = data
        cls.var_event.set()



