# -*- coding: utf-8
from tkinter_frontend.window_root.frame_1.frame_for_options.build import frame_for_options
from tkinter import ttk, StringVar, font, W
from objects import config

choice = StringVar()
style = ttk.Style()
font_radio_b = font.Font(size=13)


style.configure("TRadiobutton", background=config.get("BACKGROUND_COLOR", "blue"),
                foreground=config.get("FOREGROUND_COLOR", "white"), font=font_radio_b)

button_1 = ttk.Radiobutton(frame_for_options, text="Сортировать по просмотрам за всё время", variable=choice,
                           value="total_views", cursor="hand2",)
button_1.grid(column=1, row=1, sticky=W)
button_1.grid_configure(padx=5, pady=5)

button_2 = ttk.Radiobutton(frame_for_options, text="Сортировать по просмотрам за сегодня", variable=choice,
                           value="today_views", cursor="hand2",)
button_2.grid(column=1, row=2, sticky=W)
button_2.grid_configure(padx=5, pady=5)

button_3 = ttk.Radiobutton(frame_for_options, text="Сортировать по количеству отзывов", variable=choice,
                           value="reviews", cursor="hand2",)
button_3.grid(column=1, row=3, sticky=W)
button_3.grid_configure(padx=5, pady=5)
#
# button_4 = ttk.Radiobutton(frame_for_options, text="Другое_2", variable=choice,
#                            value="ofter_2", cursor="hand2",)
# button_4.grid(column=1, row=4, sticky=W)
# button_4.grid_configure(padx=5, pady=5)


choice.set("total_views")
