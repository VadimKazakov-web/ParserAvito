# -*- coding: utf-8 -*-
from tkinter_frontend.handlers.validation import ValidationVarClass
from settings import WIDTH_LABEL
from objects import connector
import datetime


class HandlersClass(ValidationVarClass):
    width_text = WIDTH_LABEL
    data = {}

    @classmethod
    def link_input_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        check = ValidationVarClass.validation_url(text=val)
        if check:
            icon.make_verified()
            label["text"] = f'Cсылка введена: \n{check[0:cls.width_text]}\n{check[cls.width_text:]}'
            cls.data["link"] = check
        else:
            icon.make_unchecked()
            label["text"] = "Недействительная ссылка, введите еще раз"

    @classmethod
    def default_filename(cls):
        val = ValidationVarClass.validation_file_name(text=ValidationVarClass.file_name)
        val = f'{val}_{cls.date_time_now()}.html'
        return val

    @classmethod
    def filename_input_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        val = ValidationVarClass.validation_file_name(text=val)
        val = f'{val}_{cls.date_time_now()}.html'
        icon.make_verified()
        label["text"] = f'Название файла: {val}'
        # abs_path = Path(os.getcwd()) / Path(val)
        cls.data["filename"] = val

    @staticmethod
    def date_time_now():
        datetime_now = str(datetime.datetime.today().strftime("%d·%m·%Y·%Hч·%Mмин"))
        return datetime_now

    @classmethod
    def count_page_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        result = ValidationVarClass.validation_pages(text=val)
        match result:
            case True:
                icon.make_verified()
                label["text"] = f'Количество страниц для сканирования: {val}'
                cls.data["count_pages"] = val
            case 'ValueError':
                icon.make_unchecked()
                label["text"] = "Значение не является целым числом, введите еще раз"
            case 'Limit':
                icon.make_unchecked()
                label["text"] = (f'Количество страниц превышает \nмаксимальное значение '
                                 f'{cls.max_pages}, введите еще раз')
            case 0:
                icon.make_unchecked()
                label["text"] = "Недопустимое количество"

    @classmethod
    def valid_all_vars(cls, *args, **kwargs):
        master = kwargs.get("master")
        if cls.data.get("link") and cls.data.get("filename") and cls.data.get("count_pages"):
            # from tkinter_frontend.window_root.frame_1.frame_for_options.radio_buttons.build import choice
            # cls.data["sorting"] = choice.get()
            connector.update_info(text="все данные введены")
            master.event_generate(connector.post_data_event)
            master.event_generate(connector.create_progress_event)
            return True
        else:
            connector.update_info(text="не все данные введены")
            return False
