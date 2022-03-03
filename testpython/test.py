# -*- coding:utf-8 -*-
# @author wuhao
# @date 2022/2/17
from functools import partial


class DBManager(object):
    """
    with的实现
    """

    def __init__(self):
        self.name = "with"

    def __enter__(self):
        print('__enter__', self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')
        return True


def getInstance():
    return DBManager()


import time


def time_pay(func):
    def inner(*args, **kwargs):
        for line in range(2):
            print(line + 1)
            time.sleep(1)
        res = func(*args, **kwargs)
        return res

    return inner


# 2s 调用一次函数
@time_pay
def func1():
    print("from func1.....")


# 一次调用5回函数调用
def again_func(func):
    def inner(*args, **kwargs):
        for line in range(5):
            func(line)

    return inner


@again_func
def func2(*args, **kwargs):
    print("func2 is going...", *args)


def multipliers():
    """闭包函数延迟问题"""
    return [lambda x, i=i: x * i for i in range(4)]


def multipliers_ch2():
    return [partial(lambda m, x: m * x, i) for i in range(4)]


if __name__ == "__main__":
    with getInstance() as dbManagerIns:
        print('with demo')
    # func2()
    # print([m(2) for m in multipliers()])
    print([m(2) for m in multipliers_ch2()])

