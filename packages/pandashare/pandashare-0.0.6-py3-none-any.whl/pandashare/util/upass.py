# -*- coding:utf-8 -*- 

"""
Created on 2024/12/23
@author: quantdrchow
@website : https://www.pandashare.pro
"""

import pandas as pd
import os
from pandashare.stock import cons as ct

def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, ct.TOKEN_F_P)
    df.to_csv(fp, index=False)
    
    
def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, ct.TOKEN_F_P)
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.loc[0]['token'])
    else:
        print(ct.TOKEN_ERR_MSG)
        return None


