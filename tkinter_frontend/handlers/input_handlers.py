# -*- coding: utf-8 -*-
from tkinter_frontend.handlers.validation import ValidationVarClass
from objects import config


class HandlersClass(ValidationVarClass):
    width_text = int(config.get("WIDTH_LABEL", 50))
    data = {}

    @classmethod
    def link_input_handler(cls, *args, **kwargs):
        link = kwargs.get("text")
        val = link.get()
        label = kwargs.get("widget")
        icon = kwargs.get("icon")
        if ValidationVarClass.validation_url(text=val):
            link.set(val)
            icon = icon.make_verified()
            label["text"] = f'Cсылка введена: \n{link.get()[0:cls.width_text]}\n{link.get()[cls.width_text:]}'
            cls.data["link"] = val
        else:
            link.set('')
            icon = icon.make_unchecked()
            label["text"] = "Недействительная ссылка, введите еще раз"

    @classmethod
    def filename_input_handler(cls, *args, **kwargs):
        filename = kwargs.get("text")
        val = filename.get()
        label = kwargs.get("widget")
        icon = kwargs.get("icon")
        val = ValidationVarClass.validation_file_name(text=val)
        filename.set(val)
        icon = icon.make_verified()
        label["text"] = f'Название файла: {filename.get()}'
        cls.data["filename"] = val

    @classmethod
    def count_page_handler(cls, *args, **kwargs):
        count = kwargs.get("text")
        val = count.get()
        label = kwargs.get("widget")
        icon = kwargs.get("icon")
        result = ValidationVarClass.validation_pages(text=val)
        match result:
            case True:
                icon = icon.make_verified()
                label["text"] = f'Количество страниц для сканирования: {val}'
                cls.data["count_pages"] = count.get()
            case 'ValueError':
                count.set('')
                icon = icon.make_unchecked()
                label["text"] = "Значение не является целым числом, введите еще раз"
            case 'Limit':
                count.set('')
                icon = icon.make_unchecked()
                label["text"] = (f'Количество страниц превышает \nмаксимальное значение '
                                 f'{cls.max_pages}, введите еще раз')
            case 0:
                icon = icon.make_unchecked()
                label["text"] = "Недопустимое количество"

    @classmethod
    def valid_all_vars(cls, *args, **kwargs):
        event = args[0]
        master = kwargs.get("master")
        master.event_generate("<<CreateProgress>>")
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
