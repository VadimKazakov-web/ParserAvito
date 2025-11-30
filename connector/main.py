# -*- coding: utf-8 -*-
import threading
import logging
from tkinter_frontend.window_root.build import ROOT as tk_interface
from objects import channel_for_variables
from tkinter_frontend.main import build_tk_interface

FORMAT = '[%(asctime)s]%(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
log = logging.getLogger(__name__)

asyncio_loop = asyncio.new_event_loop()
parser = ParserAvito(channel_for_variables=channel_for_variables)

asyncio.run_coroutine_threadsafe(parser.start(), asyncio_loop)
thread_asyncio_loop = threading.Thread(daemon=True, target=lambda: asyncio_loop.run_forever())

thread_asyncio_loop.start()
build_tk_interface()
tk_interface.mainloop()

