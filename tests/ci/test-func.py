#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Author: Kun Huang <academicgareth@gmail.com>

def hk0():
    return 0

print hk0()

def hk1(a):
    b = a*a
    return b

print hk1(3) # 9

def hk2(a, *args):
    b = a * len(args)
    return b

print hk2(5, 'a', 'b', 'c') # 10

def hk3(a, **kw):
    b = a * kw.get('b')
    return b

print hk3(6, b=3) # 18

def hk4(a, b, *args):
    c = a * b * len(args)
    return c

print hk4(2, 3, 'b')  #12
