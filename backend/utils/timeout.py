# -*- coding: utf-8 -*-
import random
import time


class TimeoutMixin:
    start = 4
    stop = 7

    def __init__(self, *args, **kwargs):
        self._events_handler = lambda: None

    def _choice_num(self) -> float:
        return round(random.uniform(self.start, self.stop), 2)
    
    def _timeout(self) -> None:
        part = 15
        chunk = self._choice_num() / part
        for i in range(0, part):
            time.sleep(chunk)
            self._events_handler()
            
    def timeout(self, *args, **kwargs):
        self._timeout()

    def timeout_add_one(self):
        self.start += 1
        self.stop += 1


