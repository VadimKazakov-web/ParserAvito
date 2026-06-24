import datetime
import threading
from tkinter_frontend.events import Events
from update.update_classs import Update


class CheckUpdateProgThread:

    """
    Класс служит для проверки, есть ли новая версия программы.
    Запускается после нажатия кнопки "проверить обновление"
    """

    first_click = None
    permissible_delta = 15

    @classmethod
    def check_jackass(cls):
        """
        Отправлять запросы на проверку о существовании новой версии можно не чаще, чем раз в cls.permissible_delta секунд
        """
        if not cls.first_click:
            cls.first_click = datetime.datetime.now()
            return True
        else:
            click = datetime.datetime.now()
            delta = click - cls.first_click
            if delta.seconds > cls.permissible_delta:
                cls.first_click = click
                return True

    @classmethod
    def start(cls, *args, **kwargs):
        cls.widget = args[0].widget
        if cls.check_jackass():
            t = threading.Thread(target=Update.check_update, daemon=True, args=(cls._update_widget,))
            t.start()

    @classmethod
    def _update_widget(cls, text, flag):
        cls.widget["text"] = text
        if flag:
            cls.widget.event_generate(Events.create_download_btn_event)


class UpdateProgThread:
    plug = None

    """
    Класс служит для изменения главного окна программы, и запуска потока с загрузкой новой версии.
    Запускается после нажатия на кнопку "загрузить новую версию"
    """

    @classmethod
    def clear_frame(cls, frame):
        for child in frame.winfo_children():
            child.destroy()

    @classmethod
    def _destroy(cls):
        from tkinter_frontend.window_root.frame_1.build import frame
        from tkinter_frontend.window_root.frame_2.build import frame_2
        cls.clear_frame(frame)
        cls.clear_frame(frame_2)
        frame_2.destroy()

    @classmethod
    def update_plug(cls, num=1):
        cls.plug["text"] += "#" * num

    @classmethod
    def _create_plug(cls):
        from tkinter_frontend.window_root.plug.build import plug
        cls.plug = plug

    @classmethod
    def start(cls, *args, **kwargs):
        cls._destroy()
        cls._create_plug()
        cls.update_plug()
        t = threading.Thread(target=Update.update, daemon=True)
        t.start()


