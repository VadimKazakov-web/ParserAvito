# -*- coding: utf-8 -*-
import re
import textwrap
from settings import WIDTH_LABEL


class Events:

    """
    Константы для генерации пользовательских событий
    """

    post_var_event = "<<PostVarEvent>>"
    post_var_event_btn = "<<PostVarEventBtn>>"
    push_start_event = "<<PushStartEvent>>"
    push_stop_event = "<<PushStopEvent>>"
    new_flow_event = "<<NewFlowEvent>>"
    info_update_event = "<<InfoUpdateEvent>>"
    window_close_event = "<<WindowCloseEvent>>"
    exit_event = "<<ExitEvent>>"
    create_download_btn_event = "<<CreateDownloadBtn>>"
    start_again_event = "<<StartAgain>>"
    exit_after_update_event = "<<ExitAfterUpdateEvent>>"


class ProgressData:

    """
    Класс служит для хранения и последующей передачи в канал информации прогресса, а именно заголовка страницы
    и кол-ва отсканированных объявлений
    """

    width_label = WIDTH_LABEL

    def __init__(self, text, num):
        try:
            self.text = self.transformation(text)
        except AttributeError as err:
            if re.search("'NoneType' object has no attribute", str(err)):
                self.text = ""
        self.num = num

    def transformation(self, text):
        # Переносит один абзац в text (строку) так, чтобы длина каждой строки не превышала width_label символов
        # https://docs.python.org/3/library/textwrap.html#textwrap.TextWrapper.wrap
        text = textwrap.fill(text=text, width=self.width_label)
        return text
