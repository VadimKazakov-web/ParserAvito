import threading
import time

data = threading.local()
data.num = 5
print(data.num)


def f():
    data.num = 4
    time.sleep(2)
    print(data.num)


t = threading.Thread(target=f)
t.start()

print(data.num)
