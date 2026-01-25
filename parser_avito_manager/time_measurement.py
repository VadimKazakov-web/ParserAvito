import datetime


class TimeMeasurementMixin:
    """
    Класс используется для измерения времени работы программы
    """

    time_start = None
    time_end = None
    time_result = None

    @classmethod
    def reset_time_start(cls):
        cls.time_start = None

    @classmethod
    def time_measurement_start(cls):
        if not cls.time_start:
            cls.time_start = datetime.datetime.today()

    @classmethod
    def time_measurement_end(cls):
        cls.time_end = datetime.datetime.today()

    @classmethod
    def time_measurement_result(cls):
        cls.time_result = cls.time_end - cls.time_start
        return str(cls.time_result)[:-7]

