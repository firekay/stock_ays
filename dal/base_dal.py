# encoding: UTF-8

from models.model import *
import tushare as ts
import logging

logger = logging.getLogger(__name__)
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'


def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989:
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True


def save_stock_basic():
    logger.info('Begin save stock basic.')
    try:
        data_df = ts.get_stock_basics()
        data_df['code'] = pd.Series(data_df.axes[0], index=data_df.index)
        data = data_df.values
        data_dicts = [{'code': row[15], 'name': row[0], 'industry': row[1], 'area': row[2], 'pe': row[3],
                       'outstanding': row[4], 'totals': row[5], 'totalAssets':row[6], 'liquidAssets':row[7],
                       'fixedAssets': row[8], 'reserved': row[9], 'reservedPerShare': row[10], 'eps': row[11],
                       'bvps': row[12], 'pb': row[13], 'timeToMarket': row[14], 'insert_date': today}
                      for row in data]
        StockBasic.insert_many(data_dicts).execute()
    except Exception:
        logger.exception('Get stock basic.')
    else:
        logger.info('Success save stock basic.')


# 业绩报告
def delete_performance_report(year, quarter):
    """删除业绩报告相应年份季度的数据
    
    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字

    """
    logger.info('Begin delete performance report data, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        PerformanceReport.delete().where(PerformanceReport.year == year,
                                           PerformanceReport.quarter == quarter)\
            .execute()
    except Exception as e:
        logger.exception('Error delete performance report data, the year is: %s, quarter is: %s'
                            % (year, quarter))
        return False
    else:
        logger.info('Success delete performance report data, the year is: %s, quarter is: %s'
                    % (year, quarter))
        return True


def get_performance_report(year, quarter):
    """得到业绩报告

    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
        """
    _check_input(year, quarter)
    logger.info('Begin get performance report data, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.get_report_data(year, quarter)
    except Exception as e:
        logging.exception('Error get performance report data, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get performance report data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'eps': row[2], 'eps_yoy': row[3], 'bvps': row[4],
                           'roe': row[5],  'epcf': row[6], 'net_profits': row[7], 'profits_yoy': row[8],
                           'distrib': row[9], 'report_date': row[10],
                           'insert_date': today} for row in data_df.values]
            logger.info('Success get performance report data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


def save_performance_report(data_dicts, year, quarter):
    """存储业绩报告"""
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save performance report data, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        PerformanceReport.insert_many(data_dicts).execute()
        logger.info('Success save performance report data, the year is: %s, quarter is: %s'
                    % (year, quarter))
        return True
    except Exception as e:
        logger.exception('Error save performance report data, the year is: %s, quarter is: %s'
                         % (year, quarter))
        return False
    pass


# 盈利能力
def delete_profit_ability(year, quarter):
    pass


def get_profit_ability(year, quarter):
    pass


def save_profit_ability(year, quarter):
    pass


# 营运能力
def delete_operation_ability(year, quarter):
    pass


def get_operation_ability(year, quarter):
    pass


def save_operation_ability(year, quarter):
    pass


# 成长能力
def delete_growth_ability(year, quarter):
    pass


def get_growth_ability(year, quarter):
    pass


def save_growth_ability(year, quarter):
    pass


# 偿债能力
def delete_pay_debt_ability(year, quarter):
    pass


def get_pay_debt_ability(year, quarter):
    pass


def save_pay_debt_ability(year, quarter):
    pass


# 现金流量
def delete_cash_flow(year, quarter):
    pass


def get_cash_flow(year, quarter):
    pass


def save_cash_flow(year, quarter):
    pass
