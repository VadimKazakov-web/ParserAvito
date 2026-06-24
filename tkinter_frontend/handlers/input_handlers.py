# -*- coding: utf-8 -*-
from tkinter_frontend.handlers.validation import ValidationVarClass
from settings import WIDTH_LABEL
import datetime
from tkinter_frontend.events import Events


class HandlersClass(ValidationVarClass):
    """
    Класс предоставляет методы-обработчики для проверки url, названия файла, кол-ва страниц
    непосредственно после ввода в соответствующие поля
    """
    width_text = WIDTH_LABEL
    data = {}

    @classmethod
    def link_input_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        url = cls.validation_url(text=val)
        if url:
            icon.make_verified()
            label["text"] = f'Ccылка введена: \n{url[0:cls.width_text]}\n{url[cls.width_text:]}'
            cls.data["url"] = url
        else:
            icon.make_unchecked()
            label["text"] = "Недействительная ссылка, введите еще раз"

    @classmethod
    def default_filename(cls):
        val = cls.validation_file_name(text=cls.file_name)
        val = f'{val}_{cls.date_time_now()}.html'
        return val

    @classmethod
    def filename_input_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        val = cls.validation_file_name(text=val)
        val = f'{val}_{cls.date_time_now()}.html'
        icon.make_verified()
        label["text"] = f'Название файла: {val}'
        cls.data["filename"] = val

    @staticmethod
    def date_time_now():
        datetime_now = str(datetime.datetime.today().strftime("%d_%m_%Y_%Hч_%Mмин"))
        return datetime_now

    @classmethod
    def count_page_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        result = cls.validation_pages(text=val)
        match result:
            case True:
                icon.make_verified()
                label["text"] = f'Количество страниц для сканирования: {val}'
                cls.data["pages"] = int(val)
            case cls._no_num:
                icon.make_unchecked()
                label["text"] = "Значение не является целым числом, введите еще раз"
            case cls._limit_num:
                icon.make_unchecked()
                label["text"] = (f'Количество страниц превышает \nмаксимальное значение '
                                 f'{cls.max_pages}, введите еще раз')
            case 0:
                icon.make_unchecked()
                label["text"] = "Недопустимое количество"

    @classmethod
    def valid_all_vars(cls, *args, **kwargs):
        if cls.data.get("url") and cls.data.get("filename") and cls.data.get("pages"):
            from tkinter_frontend.window_root.frame_1.frame_for_buttons.start_button.build import button_instance as start_btn
            from tkinter_frontend.window_root.frame_1.frame_for_buttons.stop_button.build import button_instance as stop_btn
            from tkinter_frontend.window_root.build import ROOT
            ROOT.event_generate(Events.post_var_event)
            cls.data["default_filename"] = cls.default_filename()
            start_btn.event_generate(Events.post_var_event_btn)
            stop_btn.event_generate(Events.post_var_event_btn)
            return True
        else:
            return False
