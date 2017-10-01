# encoding: UTF-8
from playhouse.pool import PooledMySQLDatabase
from peewee import *
__host = "localhost"
__port = 3306
__database = "stock_ays"
__user = "root"
__passwd = "kay"

database = PooledMySQLDatabase(database=__database, max_connections=3,
                               stale_timeout=120, host=__host, port=int(__port),
                               user=__user, passwd=__passwd, charset='utf8')


class BaseModel(Model):
    class Meta:
        database = database


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

StockBasic.select(StockBasic.code).where(StockBasic.timeToMarket != 0).order_by(StockBasic.code)
