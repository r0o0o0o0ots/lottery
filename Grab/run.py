# -*-coding:utf-8 -*-
__author__ = 'ZZ'
from functools import wraps
import time
from viewer.Grabber import *

def timet(func):
    @wraps(func)
    def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print "\n########################\nused: %.2f seconds" % (end-start,)
        return result
    return wrapper

@timet
def grabFootballMatch():
    gber = Grabber("www.sporttery.cn")
    gber.analyse()


if __name__ == '__main__':
    grabFootballMatch()