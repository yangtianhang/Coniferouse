# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'


s = set()
with open("/Users/yangtianhang/mycodes/ConiferousClient/t1.out") as f1:
    for v in f1:
        if v in s:
            print "same: " + v
        s.add(v)

with open("/Users/yangtianhang/mycodes/ConiferousClient/t2.out") as f2:
    for v in f2:
        if v in s:
            print "same: " + v
        s.add(v)

print "done: " + str(len(s))