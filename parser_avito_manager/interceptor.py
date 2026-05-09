import re


class InterceptorMixin:

    cookie_dict = {}

    @classmethod
    def interceptor_req(cls, request):
        del request.headers['accept']
        request.headers['accept'] = ('text/html,application/xhtml+xml,application/xml;q=0.9,'
                                     'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;'
                                     'v=b3;q=0.7')

        del request.headers['sec-ch-ua']
        request.headers['sec-ch-ua'] = '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"'

        # del request.headers['accept-encoding']
        # request.headers['accept-encoding'] = 'gzip, deflate, br, zstd'

        # del request.headers['accept-language']
        # request.headers['accept-language'] = 'ru,en;q=0.9'

        # del request.headers['referer']
        # request.headers['referer'] = self.url

        del request.headers['cookie']
        request.headers['cookie'] = cls._cookie_dict_in_str()

    @classmethod
    def interceptor_res(cls, request, response):
        for key, val in response.headers.items():
            if key == "set-cookie" or key == "Set-Cookie":
                cls._update_cookie_dict(text=val)

    @classmethod
    def _update_cookie_dict(cls, text: str, init=False):
        value_list = text.split("; ")
        if not init:
            value = value_list[0]
            cls._str_in_cookie_dict(value)
        else:
            for elem in value_list:
                cls._str_in_cookie_dict(elem)

    @classmethod
    def _str_in_cookie_dict(cls, text):
        match = re.match(r"(?P<key>.+?)=(?P<val>.*)", text)
        key, val = match.group("key"), match.group("val")
        cls.cookie_dict[key] = val

    @classmethod
    def _cookie_dict_in_str(cls):
        intermediate_list = []
        if cls.cookie_dict:
            for key, val in cls.cookie_dict.items():
                intermediate_list.append(f"{key}={val}")
            result = "; ".join(intermediate_list)
            return result
