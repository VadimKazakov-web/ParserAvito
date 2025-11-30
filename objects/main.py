# -*- coding: utf-8 -*-
import queue
from dotenv import dotenv_values

config = dotenv_values(".env.interface")
channel_for_variables = queue.Queue()
