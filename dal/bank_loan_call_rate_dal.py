# encoding: UTF-8

import tushare as ts
import logging
from utils import util

logger = logging.getLogger(__name__)


def get_shibor_rate(year=None):
    """上海银行间同业拆放利率（Shanghai Interbank Offered Rate，简称Shibor）
    
    Args:
        year: 年份(YYYY),默认为当前年份
    """
    if not year:
        year = util.get_year()
    logger.info('Begin get ShiborRate, year is: %s.' % year)
    try:
        data_df = ts.shibor_data(year)
    except Exception as e:
        logger.exception('Error get ShiborRate. year is: %s.' % year)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get ShiborRate. year is: %s.' % year)
        else:
            data_df['date'] = data_df['date'].astype(str)
            data_dicts = [{'date': row[0], 'ON': row[1],
                           'W1': row[2], 'W2': row[3], 'M1': row[4],
                           'M3': row[5], 'M6': row[6], 'M9': row[7], 'Y1': row[8],
                           'year': year}
                          for row in data_df.values]
            logger.info('Success get ShiborRate. year is: %s.' % year)
        return data_dicts


def get_shibor_quote(year=None):
    """银行报价数据

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    if not year:
        year = util.get_year()
    logger.info('Begin get ShiborQuote, year is: %s.' % year)
    try:
        data_df = ts.shibor_quote_data(year)
    except Exception as e:
        logger.exception('Error get ShiborQuote. year is: %s.' % year)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get ShiborQuote. year is: %s.' % year)
        else:
            data_df['date'] = data_df['date'].astype(str)
            data_dicts = [{'date': row[0], 'bank': row[1],
                           'ON': row[2], 'ON_B': row[3], 'ON_A': row[4],
                           'W1_B': row[5], 'W1_A': row[6], 'W2_B': row[7], 'W2_A': row[8],
                           'M1_B': row[9], 'M1_A': row[10], 'M3_B': row[11],
                           'M3_A': row[12], 'M6_B': row[13], 'M6_A': row[14],
                           'M9_B': row[15], 'M9_A': row[16], 'Y1_B': row[17], 'Y1_A': row[18],
                           'year': year}
                          for row in data_df.values]
            logger.info('Success get ShiborQuote. year is: %s.' % year)
        return data_dicts


def get_shibor_ma(year=None):
    """Shibor均值数据（Shanghai Interbank Offered Rate，简称Shibor）

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    if not year:
        year = util.get_year()
    logger.info('Begin get ShiborMA, year is: %s.' % year)
    try:
        data_df = ts.shibor_ma_data(year)
    except Exception as e:
        logger.exception('Error get ShiborMA. year is: %s.' % year)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get ShiborMA. year is: %s.' % year)
        else:
            data_df['date'] = data_df['date'].astype(str)
            data_dicts = [{'date': row[0], 'on_5': row[1],
                           'on_10': row[2], 'on_20': row[3], 'W1_5': row[4],
                           'W1_10': row[5], 'W1_20': row[6], 'W2_5': row[7], 'W2_10': row[8],
                           'W2_20': row[9], 'M1_5': row[10], 'M1_10': row[11],
                           'M1_20': row[12], 'M3_5': row[13], 'M3_10': row[14],
                           'M3_20': row[15], 'M6_5': row[16], 'M6_10': row[17], 'M6_20': row[18],
                           'M9_5': row[19], 'M9_10': row[20], 'M9_20': row[21], 'Y1_5': row[22],
                           'Y1_10': row[23], 'Y1_20': row[24],
                           'year': year}
                          for row in data_df.values]
            logger.info('Success get ShiborMA. year is: %s.' % year)
        return data_dicts


def get_lpr(year=None):
    """贷款基础利率（LPR）（Shanghai Interbank Offered Rate，简称Shibor）

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    if not year:
        year = util.get_year()
    logger.info('Begin get LPR, year is: %s.' % year)
    try:
        data_df = ts.lpr_data(year)
    except Exception as e:
        logger.exception('Error get LPR. year is: %s.' % year)
        return None
    else:
        data_df['date'] = data_df['date'].astype(str)
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get LPR. year is: %s.' % year)
        else:
            data_df['date'] = data_df['date'].astype(str)
            data_dicts = [{'date': row[0], 'Y1': row[1], 'year': year}
                          for row in data_df.values]
            logger.info('Success get LPR. year is: %s.' % year)
        return data_dicts


def get_lpr_ma(year=None):
    """上海银行间同业拆放利率（Shanghai Interbank Offered Rate，简称Shibor）

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    if not year:
        year = util.get_year()
    logger.info('Begin get LprMA, year is: %s.' % year)
    try:
        data_df = ts.lpr_ma_data(year)
    except Exception as e:
        logger.exception('Error get LprMA. year is: %s.' % year)
        return None
    else:
        data_df['date'] = data_df['date'].astype(str)
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get LprMA. year is: %s.' % year)
        else:
            data_df['date'] = data_df['date'].astype(str)
            data_dicts = [{'date': row[0], 'Y1_5': row[1],
                           'Y1_10': row[2], 'Y1_20': row[3], 'year': year}
                          for row in data_df.values]
            logger.info('Success get LprMA. year is: %s.' % year)
        return data_dicts

