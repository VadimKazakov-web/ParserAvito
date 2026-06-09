# -*- coding: utf-8 -*-
import random
import time


class TimeoutMixin:

    """
    Класс используется для задания таймаута на странице. В месте yield метода _timeout проверяются некоторые события,
    сделано для повышения отзывчивости программы
    """

    start = 4
    stop = 7

    @classmethod
    def _choice_num(cls) -> float:
        return round(random.uniform(cls.start, cls.stop), 2)

    @classmethod
    def _timeout(cls) -> None:
        part = 10
        chunk = cls._choice_num() / part
        for i in range(0, part):
            time.sleep(chunk)
            yield
            
    def timeout(self, *args, **kwargs):
        yield from self._timeout()

    @classmethod
    def timeout_add_one(cls):
        cls.start += 1
        cls.stop += 1


