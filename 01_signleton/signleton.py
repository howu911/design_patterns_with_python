# 元类的方式
# http://www.blackedu.vip/892/dan-li-mo-shi-python-she-ji-mo-shi-yi/

class MetaSingle(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaSingle, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Logger(metaclass=MetaSingle):
    pass

def main1():
    logger1 = Logger()
    logger2 = Logger()
    print(logger1)
    print(logger2)


# 线程安全
from threading import Lock

class MetaSingle(type):
    _instance = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instance:
                cls._instance[cls] = super(MetaSingle, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


# 其他方式：
# https://blog.csdn.net/alion_x/article/details/127127574

# python父类看不到子类的函数
class S:
    def a(self):
        print("a")

class C(S):
    def b(self):
        print("b")

def main2():
    s = C()
    s.a()

if __name__ == "__main__":
    main2()