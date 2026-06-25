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
    def _choice_num(cls) -> int:
        return random.randint(cls.start, cls.stop)

    @classmethod
    def _timeout(cls) -> None:
        num = cls._choice_num()
        divider = num * 2
        part = int(num / divider)
        for chunk in range(0, part):
            time.sleep(chunk)
            yield
            
    def timeout(self, *args, **kwargs):
        yield from self._timeout()

    @classmethod
    def timeout_add_one(cls):
        cls.start += 1
        cls.stop += 1


