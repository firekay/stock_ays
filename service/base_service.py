# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import base_dal
from dal import util_dal
from utils import util

logger = logging.getLogger(__name__)


def save_stocks_basic_data(day=None):
    """股票列表"""
    insert_date = day if day else get_today_line()
    util_dal.delete_insert_date_data(StockBasic, insert_date)
    base_dal.save_stock_basic(insert_date)


def get_max_stock(insert_date):
    """获取最大股票"""
    stocks = get_stocks(insert_date).order_by(StockBasic.code.desc()).limit(1)
    max_stock = [stock.code for stock in stocks][0]
    return max_stock


def get_stocks(insert_date):
    """获取股票列表"""
    insert_date = insert_date if insert_date >= '2017-10-11' else '2017-10-11'
    # 过滤没有上市的股票, 没有过滤停盘的股票
    stock_count = StockBasic.select(StockBasic.code)\
        .where(StockBasic.insert_date == insert_date, StockBasic.timeToMarket != 0)\
        .count()
    if stock_count < 2000:
        logger.warn('No enough stocks in this day, the date is: %s, the stock count is: %s.'
                    % (insert_date, stock_count))
        before_day = util.date2str(util.str2date(insert_date) + datetime.timedelta(days=-1))
        logger.info('Will get before day stocks, the date is: %s.' % before_day)
        return get_stocks(before_day)
    else:
        return StockBasic.select(StockBasic.code) \
            .where(StockBasic.insert_date == insert_date, StockBasic.timeToMarket != 0) \
            .order_by(StockBasic.code)


def load_stocks_before_entering_date(open_date, insert_date=base_dal.today_line):
    """得到小于给定入市时间的股票列表
    
    Args:
        open_date: 入市时间, 格式: YYYYMMDD
        insert_date: 插入时间(指定哪一天的股票), 格式: YYYY-MM-DD
    """
    stock_count = base_dal.load_stock_count(insert_date)
    if stock_count < 2000:
        logger.warn('No enough stocks in this day, the date is: %s, the stock count is: %s.'
                    % (insert_date, stock_count))
        before_insert_day = util.date2str(util.str2date(insert_date) + datetime.timedelta(days=-1))
        return load_stocks_before_entering_date(open_date, before_insert_day)
    else:
        return base_dal.load_stocks_before_entering_date(open_date, insert_date)


def save_performance_report(year, quarter):
    """业绩报告（主表）
    
    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    """
    year = util.get_year() if year is None else year
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
    year = util.get_year() if year is None else year
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
    year = util.get_year() if year is None else year
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
    year = util.get_year() if year is None else year
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
    year = util.get_year() if year is None else year
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
    year = util.get_year() if year is None else year
    data_dicts = base_dal.get_cash_flow(year, quarter)
    if data_dicts:
        if util_dal.delete_year_quarter_data(CashFlow, year, quarter):
            util_dal.save_year_quarter_data(CashFlow, data_dicts, year, quarter)
