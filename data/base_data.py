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
    """stock list"""
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
    def create_tbl(self):
        # connect()
        StockBasic.create_table()
        # close()

