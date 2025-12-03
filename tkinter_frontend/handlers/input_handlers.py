# -*- coding: utf-8 -*-
from tkinter_frontend.handlers.validation import ValidationVarClass
from objects import config


class HandlersClass(ValidationVarClass):
    width_text = int(config.get("WIDTH_LABEL", 50))
    data = {}

    @classmethod
    def link_input_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        if ValidationVarClass.validation_url(text=val):
            icon.make_verified()
            label["text"] = f'Cсылка введена: \n{val[0:cls.width_text]}\n{val[cls.width_text:]}'
            cls.data["link"] = val
        else:
            icon.make_unchecked()
            label["text"] = "Недействительная ссылка, введите еще раз"

    @classmethod
    def filename_input_handler(cls, *args, **kwargs):
        entry = kwargs.get("entry")
        val = entry.get()
        label = kwargs.get("label")
        icon = kwargs.get("icon")
        entry.set('')
        val = ValidationVarClass.validation_file_name(text=val)
        icon.make_verified()
        label["text"] = f'Название файла: {val}'
        cls.data["filename"] = val

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
        if cls.data.get("link") and cls.data.get("filename") and cls.data.get("count_pages"):
            button_custom = kwargs.get("widget")
            master = kwargs.get("master")
            button = button_custom.get_instance()
            button["background"] = "#808080"
            button["cursor"] = "arrow"
            button.unbind("<ButtonPress-1>")
            button_custom.delete_hover()
            master.event_generate("<<PostData>>")
            master.event_generate("<<UnbindReturn>>")
            master.event_generate("<<CreateProgress>>")
            return True
        else:
            return False
