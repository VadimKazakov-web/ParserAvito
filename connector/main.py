# -*- coding: utf-8 -*-
from objects.data_for_progress import DataForProgress


class Connector:
    def __init__(self):
        self.data = DataForProgress()
        self.post_data_event = "<<PostData>>"
        self.create_progress_event = "<<CreateProgress>>"
        self.update_info_event = "<<UpdateInfo>>"
        self.update_progress_event = "<<UpdateProgress>>"
        self.push_button_event = "<<PushButton>>"

    def update_info(self, widget, text):
        self.data.set(key="info", val=text)
        widget.event_generate(self.update_info_event)

    def update_progress(self, widget, text):
        self.data.set(key="progress", val=text)
        widget.event_generate(self.update_progress_event)

    def update_title(self, widget, text):
        self.data.set(key="page_title", val=text)
        widget.event_generate(self.update_progress_event)

    def get_info(self):
        return self.data.get(key="info")

    def get_progress(self):
        return self.data.get(key="progress")

    def get_title(self):
        return self.data.get(key="page_title")
