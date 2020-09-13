"""
coding: utf8
@time: 2020/9/13 23:10
@author: cjr
@file: 装饰器.py
"""
import time
from functools import wraps

"""
区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
容器序列：可放多种数据类型
扁平序列：只容纳一种数据类型

list   容器序列，可变
tuple  容器序列，不可变
str    扁平序列，不可变
dict   容器序列，可变
collections.deque   容器序列，可变
"""


def get_func_run_time(func):
    """
    计算函数运行时间
    :param args:
    :param kwargs:
    :return:
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # print(func.__name__)
        start = time.time()
        略略略 = func(*args, **kwargs)
        end = time.time()
        result = end - start
        print(result)
        return 略略略
    return decorated_function


@get_func_run_time
def my_map(func, itea):
    """
    自定义一个简单的map()
    :param func:
    :param itea:
    :return:
    """
    res = []
    for i in itea:
        res.append(func(i))
    return res


def my_func(x):
    """
    测试用的
    :param x:
    :return:
    """
    time.sleep(0.2)
    return x**2


if __name__ == '__main__':
    list1 = [1, 2, 3]
    res = my_map(my_func, list1)
    print(res)
