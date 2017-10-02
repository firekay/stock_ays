# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import base_dal
from dal import util_dal

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
        if util_dal.delete_year_quarter_data(PerformanceReport, year, quarter):
            util_dal.save_data(PerformanceReport, data_dicts, year, quarter)


def save_profit_ability(year, quarter):
    data_dicts = base_dal.get_profit_ability(year, quarter)
    if not data_dicts.empty:
        if util_dal.delete_year_quarter_data(ProfitAbility, year, quarter):
            util_dal.save_data(ProfitAbility, year, quarter)


def save_operation_ability(year, quarter):
    data_dicts = base_dal.get_operation_ability(year, quarter)
    if not data_dicts.empty:
        if util_dal.delete_year_quarter_data(OperationAbility, year, quarter):
            util_dal.save_data(OperationAbility, year, quarter)


def save_growth_ability(year, quarter):
    data_dicts = base_dal.get_growth_ability(year, quarter)
    if not data_dicts.empty:
        if util_dal.delete_year_quarter_data(GrowthAbility, year, quarter):
            util_dal.save_data(GrowthAbility, year, quarter)


def save_pay_debt_ability(year, quarter):
    data_dicts = base_dal.get_pay_debt_ability(year, quarter)
    if not data_dicts.empty:
        if util_dal.delete_year_quarter_data(PayDebtAbility, year, quarter):
            util_dal.save_data(PayDebtAbility, year, quarter)


def save_cash_flow(year, quarter):
    data_dicts = base_dal.get_cash_flow(year, quarter)
    if not data_dicts.empty:
        if util_dal.delete_year_quarter_data(CashFlow, year, quarter):
            util_dal.save_data(CashFlow, year, quarter)
