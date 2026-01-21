# -*- coding: utf-8 -*-
from connector.client import ClientMixin
from objects.data_for_progress import DataForProgress
from tkinter import Widget


class Connector(ClientMixin):

    """
    Класс, который реализует в основном логику взаимодействия между "бэкендом" и интерфейсом tkinter.
    В классе ParserAvitoManager записываются данные в объект DataForProgress и генерируются пользовательские события
    на виджете, а в интерфейсе tkinter обрабатываются события, читаются и отображаются данные.
    """

    def __init__(self):
        self.data = DataForProgress()
        self.post_data_event = "<<PostData>>"
        self.create_progress_event = "<<CreateProgress>>"
        self.update_info_event = "<<UpdateInfo>>"
        self.update_progress_event = "<<UpdateProgress>>"
        self.push_button_event = "<<PushButton>>"
        self.exit_flag = False
        self.widget = None

    def add_widget(self, widget: Widget):
        self.widget = widget

    def update_info(self, text: str) -> None:
        self.data.set(key="info", val=text)
        self.widget.event_generate(self.update_info_event)

    def update_progress(self, text: str) -> None:
        self.data.set(key="progress", val=text)
        self.widget.event_generate(self.update_progress_event)

    def update_title(self, text: str) -> None:
        self.data.set(key="page_title", val=text)
        self.widget.event_generate(self.update_progress_event)

    def get_info(self) -> None:
        return self.data.get(key="info")

    def get_progress(self) -> None:
        return self.data.get(key="progress")

    def get_title(self) -> None:
        return self.data.get(key="page_title")

    def post_data(self, *args, **kwargs):
        super().post_data(*args, **kwargs)
        try:
            widget = args[0].widget
        except IndexError:
            pass
        else:
            widget.event_generate(self.push_button_event)
