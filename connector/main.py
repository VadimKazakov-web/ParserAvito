# -*- coding: utf-8 -*-
class Connector:
    def __init__(self, data):
        self.data = data
        self.update_info_event = "<<UpdateInfo>>"
        self.update_progress_event = "<<UpdateProgress>>"

    def update_info(self, widget, text):
        self.data.set(key="info", val=text)
        widget.event_generate(self.update_info_event)

    def update_progress(self, widget, text):
        self.data.set(key="progress", val=text)
        widget.event_generate(self.update_progress_event)

    def update_title(self, widget, text):
        self.data.set(key="page_title", val=text)
        widget.event_generate(self.update_progress_event)
