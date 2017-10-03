# encoding: UTF-8

import tushare as ts
import logging
from constants import *
from models.model import *

logger = logging.getLogger(__name__)
today_line = get_today_line()


def get_top_list(date, retry_count=RETRY_COUNT, pause=PAUSE):
    """每日龙虎榜列表"""

    logger.info('Begin get TopList. Date is: %s.' % date)
    try:
        data_df = ts.top_list(date, retry_count, pause)
    except Exception as e:
        logger.exception('Error get TopList. Date is: %s.' % date)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get TopList. Date is: %s.' % date)
        else:
            data_dicts = [{'code': row[0], 'name': row[1],
                           'pchange': row[2], 'amount': row[3], 'buy': row[4],
                           'sell': row[5], 'reason': row[6], 'bratio': row[7],
                           'sratio': row[8], 'date': row[9]}
                          for row in data_df.values]
            logger.info('Success get TopList. Date is: %s.' % date)
        return data_dicts


def get_individual_statistics_tops(days=5, retry_count=RETRY_COUNT, pause=PAUSE):
    """个股上榜统计"""

    logger.info('Begin get IndividualStatisticsTops. Days is: %s.' % days)
    try:
        data_df = ts.cap_tops(days, retry_count, pause)
    except Exception as e:
        logger.exception('Error get IndividualStatisticsTops. Days is: %s.' % days)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get IndividualStatisticsTops. Days is: %s.' % days)
        else:
            data_dicts = [{'code': row[0], 'name': row[1],
                           'count': row[2], 'bamount': row[3], 'samount': row[4],
                           'net': row[5], 'bcount': row[6], 'scount': row[7],
                           'days_type': days, 'insert_date': today_line}
                          for row in data_df.values]
            logger.info('Success get IndividualStatisticsTops. Days is: %s.' % days)
        return data_dicts


def get_broker_tops(days=5, retry_count=RETRY_COUNT, pause=PAUSE):
    """营业部上榜统计"""

    logger.info('Begin get BrokerTops. Days is: %s.' % days)
    try:
        data_df = ts.broker_tops(days, retry_count, pause)
    except Exception as e:
        logger.exception('Error get BrokerTops. Days is: %s.' % days)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get BrokerTops. Days is: %s.' % days)
        else:
            data_dicts = [{'broker': row[0], 'count': row[1],
                           'bamount': row[2], 'bcount': row[3], 'samount': row[4],
                           'scount': row[5], 'top3': row[6],
                           'days_type': days, 'insert_date': today_line}
                          for row in data_df.values]
            logger.info('Success get BrokerTops. Days is: %s.' % days)
        return data_dicts


def get_institution_tops(days=5, retry_count=RETRY_COUNT, pause=PAUSE):
    """机构成交明细"""

    logger.info('Begin get InstitutionTops. Days is: %s.' % days)
    try:
        data_df = ts.inst_tops(days, retry_count, pause)
    except Exception as e:
        logger.exception('Error get InstitutionTops. Days is: %s.' % days)
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get InstitutionTops. Days is: %s.' % days)
        else:
            data_dicts = [{'code': row[0], 'name': row[1],
                           'bamount': row[2], 'bcount': row[3], 'samount': row[4],
                           'scount': row[5], 'net': row[6],
                           'days_type': days, 'insert_date': today_line}
                          for row in data_df.values]
            logger.info('Success get InstitutionTops. Days is: %s.' % days)
        return data_dicts


def get_institution_detail(retry_count=RETRY_COUNT, pause=PAUSE):
    """机构成交明细"""

    logger.info('Begin get InstitutionDetail.')
    try:
        data_df = ts.inst_detail(retry_count, pause)
    except Exception as e:
        logger.exception('Error get InstitutionDetail.')
        return None
    else:
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get InstitutionDetail.')
        else:
            data_dicts = [{'code': row[0], 'name': row[1],
                           'deal_date': row[2], 'bamount': row[3], 'samount': row[4],
                           'type': row[5], 'insert_date': today_line}
                          for row in data_df.values]
            logger.info('Success get InstitutionDetail.')
        return data_dicts


