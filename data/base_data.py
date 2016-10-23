# encoding: UTF-8

from peewee import *
from utils.mysql_utils import *
from utils.util import *
import tushare as ts
import pandas as pd


today = str(get_today())
class BaseModel(Model):
    class Meta:
        database = database        
        

class StockBasic(BaseModel):
    """概念分类"""
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
    timeToMarket = DateField('%Y%m%d')
    insert_date =  DateField('%Y%m%d')

    @conn
    def create_tbl():
        # connect()
        StockBasic.create_table()
        # close()

    @conn
    def save_data():
        data_df = ts.get_stock_basics()
        data_df['code'] = pd.Series(data_df.axes[0], index=data_df.index)
        data = data_df.values
        print(data)
        data_dicts = [ {'code': row[15], 'name': row[0], 'industry': row[1], 'area': row[2], 'pe': row[3], 'outstanding': row[4], 'totals': row[5], 'totalAssets':row[6], 'liquidAssets':row[7], 'fixedAssets': row[8], 'reserved': row[9], 'reservedPerShare': row[10], 'eps': row[11], 'bvps': row[12], 'pb': row[13], 'timeToMarket': row[14], 'insert_date': today} for row in data ]
        # connect()
        StockBasic.insert_many(data_dicts).execute()
        # close()
