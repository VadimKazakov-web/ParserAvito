# -*- coding: utf-8 -*-
import threading
from exceptions import PushStopButton


class EventsConnector:
    push_stop_event = threading.Event()
    window_close_event = threading.Event()

    @classmethod
    def push_stop(cls):
        cls.push_stop_event.set()

    @classmethod
    def events_handler(cls):
        if cls.push_stop_event.is_set():
            cls.push_stop_event.clear()
            raise PushStopButton

    @classmethod
    def window_close(cls):
        cls.window_close_event.set()

    @classmethod
    def window_close_wait(cls):
        cls.window_close_event.wait()
        cls.window_close_event.clear()

