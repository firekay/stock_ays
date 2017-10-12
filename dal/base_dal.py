# encoding: UTF-8

from models.model import *
import pandas as pd
import tushare as ts
import logging

logger = logging.getLogger(__name__)
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'
today_line = get_today_line()


def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989:
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True


def save_stock_basic(day=None):
    logger.info('Begin get and save StockBasic.')
    insert_date = day if day else today_line

    try:
        data_df = ts.get_stock_basics()
        data_df['code'] = pd.Series(data_df.axes[0], index=data_df.index)
        data = data_df.values
        data_dicts = [{'code': row[22], 'name': row[0], 'industry': row[1], 'area': row[2], 'pe': row[3],
                       'outstanding': row[4], 'totals': row[5], 'totalAssets':row[6], 'liquidAssets':row[7],
                       'fixedAssets': row[8], 'reserved': row[9], 'reservedPerShare': row[10], 'eps': row[11],
                       'bvps': row[12], 'pb': row[13], 'timeToMarket': row[14], 'undp': row[15],
                       'perundp':row[16], 'rev': row[17], 'profit': row[18], 'gpr': row[19],
                       'npr': row[20], 'holders': row[21], 'insert_date': insert_date}
                      for row in data]
        StockBasic.insert_many(data_dicts).execute()
    except Exception:
        logger.exception('Error get and save StockBasic.')
    else:
        logger.info('Success get and save StockBasic.')


def get_performance_report(year, quarter):
    """得到业绩报告

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
        """
    _check_input(year, quarter)
    logger.info('Begin get PerformanceReport data, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_report_data(year, quarter)
    except Exception as e:
        logging.exception('Error get PerformanceReport data, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get PerformanceReport data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'eps': row[2], 'eps_yoy': row[3], 'bvps': row[4],
                           'roe': row[5],  'epcf': row[6], 'net_profits': row[7], 'profits_yoy': row[8],
                           'distrib': row[9], 'report_date': row[10],
                           'insert_date': today_line} for row in data_df.values]
            logger.info('Success get PerformanceReport data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


def get_profit_ability(year, quarter):
    """得到盈利能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
        """
    _check_input(year, quarter)
    logger.info('Begin get ProfitAbility, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_profit_data(year, quarter)
    except Exception as e:
        logging.exception('Error get ProfitAbility, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'roe': row[2], 'net_profit_ratio': row[3], 'gross_profit_rate': row[4],
                           'net_profits': row[5], 'eps': row[6], 'business_income': row[7], 'bips': row[8],
                           'insert_date': today_line} for row in data_df.values]
            logger.warn('Empty get ProfitAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            logger.info('Success get ProfitAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


def get_operation_ability(year, quarter):
    """得到营运能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
        """
    _check_input(year, quarter)
    logger.info('Begin get OperationAbility, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_operation_data(year, quarter)
    except Exception as e:
        logging.exception('Error get OperationAbility, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get OperationAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'arturnover': row[2], 'arturndays': row[3], 'inventory_turnover': row[4],
                           'inventory_days': row[5], 'currentasset_turnover': row[6], 'currentasset_days': row[7],
                           'insert_date': today_line} for row in data_df.values]

            logger.info('Success get OperationAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


def get_growth_ability(year, quarter):
    """得到成长能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
        """
    _check_input(year, quarter)
    logger.info('Begin get GrowthAbility, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_growth_data(year, quarter)
    except Exception as e:
        logging.exception('Error get GrowthAbility, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get GrowthAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'mbrg': row[2], 'nprg': row[3], 'nav': row[4],
                           'targ': row[5], 'epsg': row[6], 'seg': row[7],
                           'insert_date': today_line} for row in data_df.values]

            logger.info('Success get GrowthAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


# 偿债能力
def get_pay_debt_ability(year, quarter):
    """得到偿债能力

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
    """
    _check_input(year, quarter)
    logger.info('Begin get PayDebtAbility, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_debtpaying_data(year, quarter)
    except Exception as e:
        logging.exception('Error get PayDebtAbility, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get PayDebtAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'currentratio': row[2], 'quickratio': row[3], 'cashratio': row[4],
                           'icratio': row[5], 'sheqratio': row[6], 'adratio': row[7],
                           'insert_date': today_line} for row in data_df.values]

            logger.info('Success get PayDebtAbility, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


# 现金流量
def get_cash_flow(year, quarter):
    """得到现金流量

     Args:
         year: 年份, YYYY格式数字
         quarter: 季度, 只能是1, 2, 3, 4的数字
     Returns:
         data_dicts: 字段的列表, return None if have exception, return empty if no data
     """
    _check_input(year, quarter)
    logger.info('Begin get CashFlow, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_cashflow_data(year, quarter)
    except Exception as e:
        logging.exception('Error get CashFlow, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get CashFlow, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'cf_sales': row[2], 'rateofreturn': row[3], 'cf_nm': row[4],
                           'cf_liabilities': row[5], 'cashflowratio': row[6],
                           'insert_date': today_line} for row in data_df.values]

            logger.info('Success get CashFlow, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


