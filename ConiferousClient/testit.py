# -*- coding: UTF-8 -*-

__author__ = 'yangtianhang'

from client import Client

c = Client("127.0.0.1")
while True:
    print c.get_id()[0]