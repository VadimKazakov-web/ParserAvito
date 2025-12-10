# -*- coding: utf-8 -*-
import queue
from dotenv import dotenv_values
from objects.data_for_progress import DataForProgress
from objects.client import Client

config = dotenv_values(".env.interface")

channel_for_variables = queue.Queue()
progress = DataForProgress()
client = Client(channel_for_variables)

