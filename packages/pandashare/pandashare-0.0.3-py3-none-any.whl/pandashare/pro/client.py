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
    __http_url = 'http://api.waditu.com/dataapi'
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
        
        client = pymongo.MongoClient('mongodb://admin:123456@16.tcp.cpolar.top:11588/') 
        db = client[f"{req_params['params']['freq']}data"]  # 替换为您的数据库名称
        collection = db['df_test']  # 这里直接写死吧，其实应该输入
        cursor = collection.find({
            'ps_code': req_params['params']['ps_code'],
            'trade_time': {'$gte': req_params['params']['start_date'], '$lte': req_params['params']['end_date']}  # 过滤指定时间区间的数据
        }).batch_size(1000)  # 每批次获取1000条数据
        documents = []
        for document in cursor:
            if '_id' in document:
                del document['_id']
            documents.append(document)
        return pd.DataFrame(documents)
    
        # res = requests.post(f"{self.__http_url}/{api_name}", json=req_params, timeout=self.__timeout)
        # if res:
        #     result = json.loads(res.text)
        #     if result['code'] != 0:
        #         raise Exception(result['msg'])
        #     data = result['data']
        #     columns = data['fields']
        #     items = data['items']
        #     return pd.DataFrame(items, columns=columns)
        # else:
        #     return pd.DataFrame()

    def __getattr__(self, name):
        return partial(self.query, name)

























