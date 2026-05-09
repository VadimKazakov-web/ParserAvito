# -*- coding: utf-8 -*-
import random
import time


class TimeoutMixin:
    start = 4
    stop = 7

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def _choice_num(cls) -> float:
        return round(random.uniform(cls.start, cls.stop), 2)
    
    @classmethod
    def _timeout(cls) -> None:
        part = 15
        chunk = cls._choice_num() / part
        for i in range(0, part):
            time.sleep(chunk)
            
    @classmethod
    def timeout(cls, *args, **kwargs):
        cls._timeout()

    @classmethod
    def timeout_add_one(cls):
        cls.start += 1
        cls.stop += 1


