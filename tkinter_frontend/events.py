# -*- coding: utf-8 -*-

class Events:
    post_var_event = "<<PostVarEvent>>"
    push_start_event = "<<PushStartEvent>>"
    push_stop_event = "<<PushStopEvent>>"
    new_flow_event = "<<NewFlowEvent>>"
    info_update_event = "<<InfoUpdateEvent>>"


class InfoUpdateEvent(Events):

    def __init__(self, data):
        self.data = data

