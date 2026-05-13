# -*- coding: utf-8 -*-
import threading
from exceptions import PushStopButton


class EventsConnector:
    push_stop_event = threading.Event()

    @classmethod
    def push_stop(cls):
        cls.push_stop_event.set()

    @classmethod
    def events_handler(cls):
        if cls.push_stop_event.is_set():
            cls.push_stop_event.clear()
            raise PushStopButton

