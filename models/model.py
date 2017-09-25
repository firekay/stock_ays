#encoding: UTF-8

from peewee import *
from utils.mysql_utils import *
from utils.util import *
import tushare as ts
import pandas as pd


today = str(get_today())


class BaseModel(Model):
    class Meta:
        database = database


# 股票分类数据
class IndustryClassified(BaseModel):
    class Meta:
        db_table = 'industry_classified'
        
    code = CharField()
    name = CharField()    
    c_name = CharField()


class ConceptClassified(BaseModel):
    """概念分类"""
    class Meta:
        db_table = 'concept_classified'
 
    code = CharField()
    name = CharField()    
    c_name = CharField()
    
    
class SmeClassified(BaseModel):
    """中小板分类"""
    class Meta:
        db_table = 'sme_classified'
        
    code = CharField()
    name = CharField()    


class AreaClassified(BaseModel):
    """地域分类"""
    class Meta:
        db_table = 'area_classified'
 
    code = CharField()
    name = CharField()    
    area = CharField()    

    
class GemClassified(BaseModel):
    """创业板分类"""
    class Meta:
        db_table = 'gem_classified'
        
    code = CharField()
    name = CharField()    

    
class StClassified(BaseModel):
    """风险警示板分类"""
    class Meta:
        db_table = 'st_classified'
        
    code = CharField()
    name = CharField()    


class Hs300(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'hs300'
        
    code = CharField()
    name = CharField()    
    date = CharField()    
    weight = CharField()    


class Sz50(BaseModel):
    """上证50成分股"""
    class Meta:
        db_table = 'sz50'
        
    code = CharField()
    name = CharField()    
 

class Zz500(BaseModel):
    """中证500成分股"""
    class Meta:
        db_table = 'zz500'
        
    code = CharField()
    name = CharField()    


class Terminated(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'terminated'
        
    code = CharField()
    name = CharField()    
    o_date = CharField()    
    t_date = CharField()    
    insert_date = CharField()    


class Suspend(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'suspend'
        
    code = CharField()
    name = CharField()    
    o_date = CharField()    
    t_date = CharField()    
    insert_date = CharField()    


# 基本面数据
class StockBasic(BaseModel):
    """股票列表"""
    class Meta:
        db_table = 'stock_basic'

    code = CharField()
    name = CharField()
    industry = CharField()
    area = CharField()
    pe = DecimalField(max_digits=12, decimal_places=2)
    outstanding = DecimalField(max_digits=12, decimal_places=2)
    totals = DecimalField(max_digits=12, decimal_places=2)
    totalAssets = DecimalField(max_digits=12, decimal_places=2)
    liquidAssets = DecimalField(max_digits=12, decimal_places=2)
    fixedAssets = DecimalField(max_digits=12, decimal_places=2)
    reserved = DecimalField(max_digits=12, decimal_places=2)
    reservedPerShare = DecimalField(max_digits=12, decimal_places=2)
    eps = DecimalField(max_digits=12, decimal_places=3)
    bvps = DecimalField(max_digits=12, decimal_places=2)
    pb = DecimalField(max_digits=12, decimal_places=2)
    timeToMarket = IntegerField()
    undp = DecimalField(max_digits=12, decimal_places=2)
    perundp = DecimalField(max_digits=12, decimal_places=2)
    rev = DecimalField(max_digits=12, decimal_places=2)
    profit = DecimalField(max_digits=12, decimal_places=2)
    gpr = DecimalField(max_digits=12, decimal_places=2)
    npr = DecimalField(max_digits=12, decimal_places=2)
    holders = DecimalField(max_digits=12, decimal_places=2)
    insert_date = DateField('%Y%m%d')


# 交易数据: 天
class HistoryDataD(BaseModel):
    """历史行情: D"""
    class Meta:
        db_table = 'history_data_d'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 =  DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=10, decimal_places=2)


# 交易数据: 周
class HistoryDataW(BaseModel):
    """历史行情:  W"""
    class Meta:
        db_table = 'history_data_w'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 =  DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=10, decimal_places=2)


# 交易数据: 月
class HistoryDataM(BaseModel):
    """历史行情:  M"""
    class Meta:
        db_table = 'history_data_m'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 =  DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=10, decimal_places=2)


class HistoryDataScd(BaseModel):
    """历史行情: 5, 15, 30, 60分钟"""
    class Meta:
        db_table = 'history_data_scd'

    code = CharField()
    ktype = CharField(5)
    date = DateField('%Y-%m-%d')
    time = TimeField('%H:%M:%S')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 =  DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=5, decimal_places=2)


class RevoteHistoryData(BaseModel):
    """复权数据"""
    class Meta:
        db_table = 'revote_history_data'

    code = CharField()
    autype = CharField(5)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    amount = DecimalField(max_digits=15, decimal_places=2)


class TodayAllData(BaseModel):
    """实时行情"""
    class Meta:
        db_table = 'today_all_data'

    code = CharField()
    name = CharField()
    date = DateField('%Y-%m-%d')
    changepercent = DecimalField(max_digits=8, decimal_places=3)
    trade = DecimalField(max_digits=8, decimal_places=2)
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    settlement = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    turnoverratio = DecimalField(max_digits=8, decimal_places=5)
    amount = DecimalField(max_digits=15, decimal_places=2)
    per = DecimalField(max_digits=10, decimal_places=4)
    mktcap = DecimalField(max_digits=15, decimal_places=2)
    nmc = DecimalField(max_digits=15, decimal_places=2)


class TickData(BaseModel):
    """历史分笔, 当日历史分笔"""
    class Meta:
        db_table = 'tick_data'

    code = CharField()
    date = DateField('%Y-%m-%d')
    time = TimeField('%H:%M:%S')
    price = DecimalField(max_digits=8, decimal_places=2)
    pchange = DecimalField(max_digits=5, decimal_places=2)
    change = DecimalField(max_digits=5, decimal_places=2)
    volume = DecimalField(max_digits=10, decimal_places=2)
    amount = DecimalField(max_digits=12, decimal_places=2)
    type = CharField()


class BigIndexData(BaseModel):
    """大盘指数行情列表"""
    class Meta:
        db_table = 'big_index'

    date = DateField('%Y-%m-%d')
    code = CharField()
    name = CharField()
    change = DecimalField(max_digits=5, decimal_places=2)
    open = DecimalField(max_digits=12, decimal_places=4)
    preclose = DecimalField(max_digits=12, decimal_places=4)
    close = DecimalField(max_digits=12, decimal_places=4)
    hign = DecimalField(max_digits=12, decimal_places=4)
    low = DecimalField(max_digits=12, decimal_places=4)
    volume = DecimalField(max_digits=10, decimal_places=2)
    amount = DecimalField(max_digits=12, decimal_places=4)


class BigTradeData(BaseModel):
    """大单交易数据"""
    class Meta:
        db_table = 'big_trade_data'

    date = DateField('%Y-%m-%d')
    code = CharField()
    name = CharField()
    time = TimeField('%H:%M:%S')
    price = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=10, decimal_places=2)
    preprice = DecimalField(max_digits=8, decimal_places=2)
    type = CharField()
