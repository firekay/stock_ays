# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import base_dal
from dal import util_dal

logger = logging.getLogger(__name__)


def save_stocks_basic_data():
    """股票列表"""
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
    """业绩报告（主表）
    
    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    """
    data_dicts = base_dal.get_performance_report(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(PerformanceReport, year, quarter):
            util_dal.save_year_quarter_data(PerformanceReport, data_dicts, year, quarter)


def save_profit_ability(year, quarter):
    """盈利能力
    
    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    """
    data_dicts = base_dal.get_profit_ability(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(ProfitAbility, year, quarter):
            util_dal.save_year_quarter_data(ProfitAbility, data_dicts, year, quarter)


def save_operation_ability(year, quarter):
    """得到营运能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    """
    data_dicts = base_dal.get_operation_ability(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(OperationAbility, year, quarter):
            util_dal.save_year_quarter_data(OperationAbility, data_dicts, year, quarter)


def save_growth_ability(year, quarter):
    """得到成长能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    """
    data_dicts = base_dal.get_growth_ability(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(GrowthAbility, year, quarter):
            util_dal.save_year_quarter_data(GrowthAbility, data_dicts, year, quarter)


def save_pay_debt_ability(year, quarter):
    """得到偿债能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    """
    data_dicts = base_dal.get_pay_debt_ability(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(PayDebtAbility, year, quarter):
            util_dal.save_year_quarter_data(PayDebtAbility, data_dicts, year, quarter)


def save_cash_flow(year, quarter):
    """得到现金流量

     Args:
         year: 年份, YYYY格式数字
         quarter: 季度, 只能是1, 2, 3, 4的数字
     Returns:
         data_dicts: 字段的列表, return None if have exception, return empty if no data
     """
    data_dicts = base_dal.get_cash_flow(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(CashFlow, year, quarter):
            util_dal.save_year_quarter_data(CashFlow, data_dicts, year, quarter)
