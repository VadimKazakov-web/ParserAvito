import threading


class DataForProgress:

    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def __str__(self):
        return self.data

    def set(self, key, val):
        self.lock.acquire()
        self.data[key] = val
        self.lock.release()

    def get(self, key):
        self.lock.acquire()
        val = self.data.get(key, "")
        self.lock.release()
        return val
