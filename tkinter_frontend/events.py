# -*- coding: utf-8 -*-
import textwrap
from settings import WIDTH_LABEL


class Events:
    post_var_event = "<<PostVarEvent>>"
    push_start_event = "<<PushStartEvent>>"
    push_stop_event = "<<PushStopEvent>>"
    new_flow_event = "<<NewFlowEvent>>"
    info_update_event = "<<InfoUpdateEvent>>"
    window_close_event = "<<WindowCloseEvent>>"
    exit_event = "<<ExitEvent>>"
    start_again_event = "<<StartAgain>>"
    exit_after_update_event = "<<ExitAfterUpdateEvent>>"


class InfoUpdateEvent:
    width_label = WIDTH_LABEL

    def __init__(self, data):
        self.text = self.transformation(data)

    def transformation(self, *args, **kwargs):
        text = ""
        if isinstance(args[0], tuple):
            if isinstance(args[0][0], str):
                text = args[0][0]
        elif isinstance(args[0], str):
            text = args[0]
        # https://docs.python.org/3/library/textwrap.html#textwrap.TextWrapper.wrap
        data = textwrap.fill(text=text, width=self.width_label)
        return data


class ProgressUpdateEvent(InfoUpdateEvent):

    def __init__(self, data):
        super().__init__(data)
        self.num = data[1]
