# encoding: UTF-8
import service.ays_data_service as adsvc
import service.data_service as dsvc
import logging
import decimal
import logging.config
from utils import util
import threading
import time
from models.model import *
import pandas as pd

logger = logging.getLogger(__name__)

#def _macd(x):
    #two_ops = []
    #factor = 0
    #for i in range(len(x)):
        #print(i)
        #factor += x[i]
        #two_ops.append(factor)
    #return two_ops   
    

def _macd(x, n_day_num):
    n_date = util.get_ndays_before_line(n_day_num)
    #factor_today = decimal.Decimal(2) / (1 + n_day_num)
    #factor_ema = decimal.Decimal(n_day_num - 1) / (1 + n_day_num)
    factor_today = float(2) / (1 + n_day_num)
    factor_ema = float(n_day_num - 1) / (1 + n_day_num)
    
    
    emas = []
    ema = 0
    print(len(x))
    print(x[0])
    for i in range(len(x)):
        ema = ema * factor_ema + float(x[i]) * factor_today
        emas.append(ema)
    return emas   


def macd_service():
    fast_d_num = 13
    slow_d_num = 27
    fast_date = util.get_ndays_before_line(fast_d_num)
    slow_date = util.get_ndays_before_line(slow_d_num)
    fast_factor = float(2) / (1 + fast_d_num)
    slow_factor = float(2) / (1 + slow_d_num)
    
    max_code = dsvc.get_max_stock()

    his_data = adsvc.get_his_data_part(slow_date, ktype='D', code=max_code)
    his_3 = his_data[:20]
    rows = []
    index = []
    for data in his_3:
        rows.append((data.open, data.close))
        index.append(data.date)
    df = pd.DataFrame(rows, columns=['open', 'close'], index=index)
    print(df)
    df_macd = df.apply(_macd, n_day_num=12)
    print(df)
    print(df_macd.values)
    print(df_macd)
