"""Декоратор на время выполнения"""

def deco_time(func):
    """Расчитывает время выполнения программы"""
    import time

    def wrap(*args):
        start = time.time()
        func(*args)
        print("Время выполнения программы", time.time() - start)

    return wrap
