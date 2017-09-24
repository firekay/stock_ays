# encoding: UTF-8
"""分析所用的数据服务， 从mysql，或者mongodb取数据"""
import sys
import traceback
import logging
import logging.config
from peewee import *
import tushare as ts
import pandas as pd
import json
from utils import mongo_utils
from utils.mysql_utils import *
from utils.util import *
import threading
import time
from models.model import *
from queue import Queue


logger = logging.getLogger(__name__)
today = get_today_line()


def get_his_data_part(date_begin, date_end=None, ktype=None, code=None):
    """获取部分历史数据.
    
    :param date: filter date. Type like '%Y-%m-%d'.
    :param ktype: 'D' 'W' 'M'
    """
    result = None
    if code is None:
        if ktype is None:
            if date_end is None:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where(HistoryData.date >= date_begin)
            else:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.date < date_end))
        else:
            assert(ktype in ['D', 'W', 'M'], "ktype must be one of 'D, W, M'.")
            if date_end is None:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.ktype == ktype))
            else:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.date < date_end) & (HistoryData.ktype == ktype))
    else:
        if ktype is None:
            if date_end is None:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.code == code))
            else:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.date < date_end)& (HistoryData.code == code))
        else:
            assert(ktype in ['D', 'W', 'M'], "ktype must be one of 'D, W, M'.")
            if date_end is None:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.ktype == ktype) & (HistoryData.code == code)).order_by(HistoryData.date)
            else:
                result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                                       HistoryData.open, HistoryData.hign,
                                       HistoryData.close, HistoryData.low,
                                       HistoryData.volume, HistoryData.price_change,
                                       HistoryData.ma5, HistoryData.ma10,
                                       HistoryData.ma20, HistoryData.v_ma5,
                                       HistoryData.v_ma10, HistoryData.v_ma20,
                                       HistoryData.turnover).where((HistoryData.date >= date_begin) & (HistoryData.date < date_end) & (HistoryData.ktype == ktype) & (HistoryData.code == code))
            #result = HistoryData.select(HistoryData.code, HistoryData.date, HistoryData.ktype, 
                               #HistoryData.open, HistoryData.hign,
                               #HistoryData.close, HistoryData.low,
                               #HistoryData.volume, HistoryData.price_change,
                               #HistoryData.ma5, HistoryData.ma10,
                               #HistoryData.ma20, HistoryData.v_ma5,
                               #HistoryData.v_ma10, HistoryData.v_ma20,
                               #HistoryData.turnover)  \
                        #.where(HistoryData.date >= date_begin &
                               #HistoryData.date < date_end &
                               #HistoryData.ktype = ktype)
    return result
        
