# -*- coding: utf-8 -*-
import queue
from dotenv import dotenv_values
from objects.client import Client
from connector import Connector

config = dotenv_values(".env.interface")
channel_for_variables = queue.Queue()
client = Client(channel_for_variables)
connector = Connector()

