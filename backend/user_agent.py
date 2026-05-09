# -*- coding: utf-8 -*-
from fake_useragent import UserAgent


class UserAgentMixin:

    _ua = UserAgent()
    _user_agent = None

    @classmethod
    def new_user_agent(cls):
        cls._user_agent = cls._ua.random
