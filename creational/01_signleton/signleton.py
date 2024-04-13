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


# 线程安全
from threading import Lock

class MetaSingleLock(type):
    _instance = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instance:
                cls._instance[cls] = super(MetaSingleLock, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


# 自己常用方法
from threading import RLock
class Singleton(object):
    single_lock = RLock()

    def __init__(self, name):
        self.name = name

    @classmethod
    def instance(cls, *args, **kwargs):
        with Singleton.single_lock:
            if not hasattr(Singleton, "_instance"):
                Singleton._instance = Singleton(*args, **kwargs)
        return Singleton._instance



# 自己常用方法（线程安全）
from threading import RLock

class Singleton(object):
    _instance = None  # 初始化为 None，用于后续的判断
    single_lock = RLock()  # 使用可重入锁

    def __init__(self, name):
        self.name = name

    @classmethod
    def instance(cls, *args, **kwargs):
        if cls._instance is None:  # 首先检查实例是否已经创建，不加锁
            with cls.single_lock:  # 锁定代码块
                if cls._instance is None:  # 再次检查，确保实例还未被创建
                    cls._instance = cls(*args, **kwargs)  # 创建实例
        return cls._instance

# 用法示例
singleton_a = Singleton.instance("Instance A")
singleton_b = Singleton.instance("Instance B")
assert singleton_a is singleton_b  # 这将验证两个变量指向同一个实例




# 其他方式：
# https://blog.csdn.net/alion_x/article/details/127127574
# https://zhuanlan.zhihu.com/p/212234792
def main():
    logger1 = Logger()
    logger2 = Logger()
    print(logger1)
    print(logger2)

if __name__ == '__main__':
    main()
