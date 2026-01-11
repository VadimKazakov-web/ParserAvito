# -*- coding: utf-8 -*-
import queue
from dotenv import dotenv_values
from connector import Connector

config = dotenv_values(".env.interface")
connector = Connector()

