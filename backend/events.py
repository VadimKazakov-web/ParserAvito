# -*- coding: utf-8 -*-
import threading


class EventsMixin:
    stop_event = threading.Event()
