# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import base_dal

logger = logging.getLogger(__name__)


def save_stocks_basic_data():
    table_service.truncate_table(StockBasic)
    base_dal.save_stock_basic()


def get_max_stock():
    """获取最大股票"""
    stocks = StockBasic.select(StockBasic.code).order_by(StockBasic.code.desc()).limit(1)
    max_sotck = [stock.code for stock in stocks][0]
    return max_sotck


def get_stocks():
    """获取股票列表"""
    # 过滤没有上市的股票
    return StockBasic.select(StockBasic.code).where(StockBasic.timeToMarket != 0).order_by(StockBasic.code)


def save_performance_report(year, quarter):
    data_df = base_dal.get_performance_report(year, quarter)