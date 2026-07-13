# -*- coding: utf-8 -*-
import asyncio
from backend.work_flow import WorkFlow


class BackendManager:

    def __init__(self, *args, **kwargs):
        pass

    def __str__(self) -> str:
        return "BackendManager"

    def __call__(self, *args, **kwargs) -> None:
        while True:
            """
            Запуск основной работы программы: открытия страниц, объявлений, сбор информации
            """
            print("-" * 10, "waiting for the start", "-" * 10)
            with WorkFlow() as work_flow:
                asyncio.run(work_flow())
