# -*- coding: utf-8 -*-
import queue
from dotenv import dotenv_values
from objects.data_for_progress import DataForProgress

config = dotenv_values(".env.interface")

channel_for_variables = queue.Queue()
data_for_prog = DataForProgress()
