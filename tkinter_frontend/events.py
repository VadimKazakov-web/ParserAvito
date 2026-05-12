# -*- coding: utf-8 -*-
import textwrap
from settings import WIDTH_LABEL


class Events:
    post_var_event = "<<PostVarEvent>>"
    push_start_event = "<<PushStartEvent>>"
    push_stop_event = "<<PushStopEvent>>"
    new_flow_event = "<<NewFlowEvent>>"
    info_update_event = "<<InfoUpdateEvent>>"


class InfoUpdateEvent(Events):

    def __init__(self, data):
        self.width_label = WIDTH_LABEL
        self.data = self.transformation(data)

    def transformation(self, *args, **kwargs):
        # https://docs.python.org/3/library/textwrap.html#textwrap.TextWrapper.wrap
        data = textwrap.fill(text=args[0], width=self.width_label)
        return data

