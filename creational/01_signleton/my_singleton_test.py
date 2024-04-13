import threading
import time
from threading import RLock

# 优化前的单例实现
class SingletonOld(object):
    _instance = None
    single_lock = RLock()

    def __init__(self, name):
        self.name = name

    @classmethod
    def instance(cls, *args, **kwargs):
        with cls.single_lock:
            if cls._instance is None:
                cls._instance = cls(*args, **kwargs)
        return cls._instance

# 优化后的单例实现
class SingletonNew(object):
    _instance = None
    single_lock = RLock()

    def __init__(self, name):
        self.name = name

    @classmethod
    def instance(cls, *args, **kwargs):
        if cls._instance is None:
            with cls.single_lock:
                if cls._instance is None:
                    cls._instance = cls(*args, **kwargs)
        return cls._instance

def test_singleton(cls, num_threads=100):
    start_time = time.time()
    threads = []
    
    def task():
        instance = cls.instance("Instance")
    
    for _ in range(num_threads):
        thread = threading.Thread(target=task)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    end_time = time.time()
    return end_time - start_time

# 测试代码
num_threads = 1000
time_old = test_singleton(SingletonOld, num_threads)
time_new = test_singleton(SingletonNew, num_threads)

print(f"Old Singleton Time: {time_old:.6f} seconds")
print(f"New Singleton Time: {time_new:.6f} seconds")
