# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import base_dal
from dal import dal_util

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
    data_dicts = base_dal.get_performance_report(year, quarter)
    if not data_dicts.empty:
        if dal_util.delete_data(PerformanceReport, year, quarter):
            dal_util.save_data(PerformanceReport, data_dicts, year, quarter)


def save_profit_ability(year, quarter):
    data_dicts = base_dal.get_profit_ability(year, quarter)
    if not data_dicts.empty:
        if dal_util.delete_data(ProfitAbility, year, quarter):
            dal_util.save_data(ProfitAbility, year, quarter)


def save_operation_ability(year, quarter):
    data_dicts = base_dal.get_operation_ability(year, quarter)
    if not data_dicts.empty:
        if dal_util.delete_data(OperationAbility, year, quarter):
            dal_util.save_data(OperationAbility, year, quarter)


def save_growth_ability(year, quarter):
    data_dicts = base_dal.get_growth_ability(year, quarter)
    if not data_dicts.empty:
        if dal_util.delete_data(GrowthAbility, year, quarter):
            dal_util.save_data(GrowthAbility, year, quarter)


def save_pay_debt_ability(year, quarter):
    data_dicts = base_dal.get_pay_debt_ability(year, quarter)
    if not data_dicts.empty:
        if dal_util.delete_data(PayDebtAbility, year, quarter):
            dal_util.save_data(PayDebtAbility, year, quarter)


def save_cash_flow(year, quarter):
    data_dicts = base_dal.get_cash_flow(year, quarter)
    if not data_dicts.empty:
        if dal_util.delete_data(CashFlow, year, quarter):
            dal_util.save_data(CashFlow, year, quarter)
