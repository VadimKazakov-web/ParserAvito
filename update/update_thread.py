import datetime
import threading
from tkinter_frontend.classes.label import Label
from update.update_classs import Update
from objects import connector


class CheckUpdateProgThread:

    first_click = None
    permissible_delta = 15

    @classmethod
    def check_jackass(cls):
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
    def reset_attr(cls):
        cls.first_click = None
        cls.second_click = None

    @classmethod
    def start(cls, *args, **kwargs):
        if cls.check_jackass():
            t = threading.Thread(target=Update.check_update)
            t.start()


class UpdateProgThread:

    @classmethod
    def clear_frame(cls, frame):
        for child in frame.winfo_children():
            child.destroy()

    @classmethod
    def create_plug(cls):
        from tkinter_frontend.window_root.frame_1.build import frame
        from tkinter_frontend.window_root.frame_2.build import frame_2
        cls.clear_frame(frame)
        cls.clear_frame(frame_2)
        frame_2.destroy()
        label = Label(master=frame, text="Загрузка...", column=0, row=0)
        label.build()

    @classmethod
    def start(cls, *args, **kwargs):
        cls.create_plug()
        connector.post_data(data="exit")
        t = threading.Thread(target=Update.update)
        t.start()

