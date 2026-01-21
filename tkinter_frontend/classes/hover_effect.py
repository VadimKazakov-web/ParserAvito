# -*- coding: utf-8 -*-
from tkinter_frontend.classes import ConfigClass


class HoverEffectMixin(ConfigClass):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.background = self.config.get("COLOR_FOR_HOVER")
        self.default_color = self.config.get("FOREGROUND_COLOR")

    def make_hover(self):
        self.instance.bind("<Enter>", func=self.hover_effect)
        self.instance.bind("<Leave>", func=self.default_effect)

    def delete_hover(self):
        self.instance.unbind("<Enter>")
        self.instance.unbind("<Leave>")

    def hover_effect(self, *args, **kwargs):
        self.instance["background"] = self.background
        return self.instance

    def default_effect(self, *args, **kwargs):
        self.instance["background"] = self.default_color
        return self.instance
