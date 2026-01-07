# -*- coding: utf-8 -*-
import threading
from exceptions import NamedParametersError


class DataForProgress:

    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def __str__(self):
        return self.data

    def set(self, *args, **kwargs):
        self.lock.acquire()
        key = kwargs.get("key")
        val = kwargs.get("val")
        if key and val:
            self.data[key] = val
        else:
            raise NamedParametersError("check parameters key or val")
        self.lock.release()

    def get(self, **kwargs):
        self.lock.acquire()
        key = kwargs.get("key")
        try:
            if key:
                val = self.data.get(key, "...")
                return val

            else:
                raise NamedParametersError("check parameters key")
        finally:
            self.lock.release()
