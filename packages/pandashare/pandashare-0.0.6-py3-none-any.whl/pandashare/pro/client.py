# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pro数据接口 
Created on 2024/12/17
@author: quantdrchow
@website : https://www.pandashare.pro
"""

import pandas as pd
import json
from functools import partial
import requests
import pymongo

class DataApi:

    __token = ''
    __http_url = 'http://16.tcp.cpolar.top:14448'
    # __http_url = 'http://127.0.0.1:8000/dataapi'

    def __init__(self, token, timeout=30):
        """
        Parameters
        ----------
        token: str
            API接口TOKEN，用于用户认证
        """
        self.__token = token
        self.__timeout = timeout

    def query(self, api_name, fields='', **kwargs):
        req_params = {
            'api_name': api_name,
            'token': self.__token,
            'params': kwargs,
            'fields': fields
        }
        url = f"{self.__http_url}/{api_name}"
        headers = {"token": self.__token}
        params = {
            "db_name": 'Astock' + kwargs['freq'],
            "ps_code": kwargs['ps_code'],
            "start_date": kwargs['start_date'],
            "end_date": kwargs['end_date'],
            "limit": kwargs['limit'],
        }
        # print(url,headers,params)
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            data = response.json()
            return pd.DataFrame(data)  # 转换为 Pandas DataFrame
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()  # 返回空的 DataFrame
        
    def __getattr__(self, name):
        return partial(self.query, name)



















