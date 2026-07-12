# -*- coding: utf-8 -*-
import asyncio
import random


def choice_num(a: int, b: int) -> int:
    """
    Возвращает случайное число от a до b

    :param a: int, нижняя граница диапазона (включительно)
    :param b: int, верхняя граница диапазона (включительно)
    :return: int, случайное число в заданном диапазоне
    """
    return random.randint(a, b)


class TimeoutMixin:

    """
    Класс используется для задания таймаута на странице. В месте yield метода timeout проверяются некоторые события,
    сделано для повышения отзывчивости программы
    """

    start = 4
    stop = 7

    @classmethod
    async def timeout(cls) -> None:
        num = choice_num(cls.start, cls.stop)
        for t in range(0, num * 3):
            await asyncio.sleep(0.33)

    @classmethod
    def timeout_add_one(cls):
        cls.start += 1
        cls.stop += 1
