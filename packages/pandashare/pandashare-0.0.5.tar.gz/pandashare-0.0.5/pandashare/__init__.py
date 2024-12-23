# -*- coding:utf-8 -*- 
# pandashare/__init__.py
import codecs
import os

__version__ = '0.0.5'
__author__ = 'quantdrchow'

def greet(name):
    return f"Hello, {name}!"

"""
for pandashare pro api
"""
from pandashare.pro.data_pro import (pro_api, pro_bar, subs, ht_subs)

"""
for utils
"""
# from pandashare.util.dateu import (trade_cal, is_holiday)

from pandashare.util.upass import (get_token, set_token)



