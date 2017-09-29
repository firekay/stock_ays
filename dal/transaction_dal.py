# encoding: UTF-8
"""调用接口得到数据，以及存入mysql， mongodb"""
import sys
import traceback
import logging
import logging.config
from peewee import *
import tushare as ts
import pandas as pd
from queue import Queue
import json
from utils import mongo_utils
from utils.mysql_utils import *
from utils.util import *
import threading
import time
from models.model import *
from service import base_service

logger = logging.getLogger(__name__)
today = get_today_line()

his_data_queue = Queue()
his_data_scd_queue = Queue()
h_revote_data_queue = Queue()
stock_k_data_queue = Queue()
tick_data_queue = Queue()
big_trade_data_queue = Queue()
RETRY_COUNT = 5
PAUSE = 0.001

max_stock = base_service.get_max_stock()


def get_stock_k_data(code, start_date=None, end_date=None, autype='qfq', index=False,
                     ktype=None, retry_count=RETRY_COUNT, pause=PAUSE):
    """从tushare得到k线数据"""
    if start_date is None or end_date is None:
        logger.info('Begin get sotck %s history k data, start date is: %s, end date is: %s.' % (code, start_date, end_date))
    else:
        logger.info('Begin get stock %s history k data, all date.' % code)
    try:
        data_df = ts.get_k_data(code, start=start_date, end=end_date, ktype=ktype, index=index,
                                retry_count=retry_count, pause=pause)
        if data_df is not None and not data_df.empty:
            data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
            data = data_df.values
            his_data_queue.put((code, ktype, autype, data))
            if start_date is None or end_date is None:
                logger.info('End get sotck %s history k data, start date is: %s, end date is: %s.' % (code, start_date, end_date))
            else:
                logger.info('End get stock %s history k data, all date.' % code)
        else:
            if start_date is None or end_date is None:
                logger.info('Empty get sotck %s history k data, start date is: %s, end date is: %s.' % (code, start_date, end_date))
            else:
                logger.info('Empty get stock %s history k data, all date.' % code)
    except Exception as e:
        if start_date is None or end_date is None:
            logger.info('Error get sotck %s history k data, start date is: %s, end date is: %s.' % (code, start_date, end_date))
        else:
            logger.info('Error get stock %s history k data, all date.' % code)


def save_stock_k_data(last_stock_code=None):
    logger.info('Begin save stock k data thread.')
    if last_stock_code:
        last_stock = last_stock_code
    else:
        last_stock = max_stock
    logger.info("Max stock code is: %s" % last_stock)
    while True:
        if h_revote_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('stock_k_data_queue\'s size is: %s' % (stock_k_data_queue.qsize()))
            stock_k_data = stock_k_data_queue.get()
            code = stock_k_data[0]
            ktype = stock_k_data[1]
            autype = stock_k_data[2]
            data = stock_k_data[3]
            logger.info('Get stock k data from stock_k_data_queue, stock code is: %s, ktype is: %s.' %
                        (code, ktype))
            data_dicts = [{'code': code, 'autype': autype, 'date': row[0], 'open':row[1],
                           'close': row[2], 'high': row[3], 'low': row[4], 'volume': row[5]} for row in data]

            try:
                # TODO: 添加5分钟, 15分钟.. 代码
                if ktype.upper() == 'D':
                    HistoryKDataD.insert_many(data_dicts).execute()
                if ktype.upper() == 'W':
                    HistoryKDataW.insert_many(data_dicts).execute()
                if ktype.upper() == 'M':
                    HistoryKDataM.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Save stock k data error. Code is: %s, ktype is: %s.' % (code, ktype))
                logger.error('Error data is: ' + data)


def save_h_revote_data(last_stock_code=None):
    logger.info('Begin save h revote data thread.')
    if last_stock_code:
        last_stock = last_stock_code
    else:
        last_stock = max_stock
    logger.info("Max stock code is: %s" % last_stock)
    while True:
        if h_revote_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('h_revote_data_queue\'s size is: %s' % (his_data_queue.qsize()))
            h_revote_data = h_revote_data_queue.get()
            code = h_revote_data[0]
            autype = h_revote_data[1]
            data = h_revote_data[2]
            logger.info('Get h revode data from h_revote_data_queue, stock code is: %s.' % code)
            try:
                data_dicts = [{'code': code, 'autype': autype, 'date': row[6], 'open': row[0], 'hign': row[1],
                               'close': row[2], 'low': row[3], 'volume': row[4], 'amount': row[5]} for row in data]
                RevoteHistoryData.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Save data error. Code is %s.' % code)
                logger.error(data)

            if code == last_stock:
                break


def get_h_revote_data(code, start_date=None, end_date=None, autype='qfp', index=False,
                      retry_count=RETRY_COUNT, pause=0, drop_factor=True):
    if start_date is None or end_date is None:
        logger.info('Begin get sotck %s h revote data, start date is: %s, end date is: %s.'
                    % (code, start_date, end_date))
    else:
        logger.info('Begin get stock %s h revote data, all date.' % code)

    try:
        data_df = ts.get_h_data(code, start_date, end_date, autype,
                                index, retry_count, pause, drop_factor)
        if data_df is not None and not data_df.empty:
            data_df['date'] = pd.Series(data_df.index, index=data_df.index)
            data = data_df.values
            h_revote_data_queue.put((code, autype, data))
            if start_date is None or end_date is None:
                logger.info('End get sotck %s h revote data, start date is: %s, end date is: %s.'
                            % (code, start_date, end_date))
            else:
                logger.info('End get stock %s h revote data, all date.' % code)
        else:
            if start_date is None or end_date is None:
                logger.info('Empty get sotck %s h revote data, start date is: %s, end date is: %s.'
                            % (code, start_date, end_date))
            else:
                logger.info('Empty get stock %s h revote data, all date.' % code)
    except Exception as e:
        if start_date is None or end_date is None:
            logger.exception('Error get sotck %s h revote data, start date is: %s, end date is: %s.'
                             % (code, start_date, end_date))
        else:
            logger.exception('Error get stock %s h revote data, all date.' % code)


def save_his_data(last_stock_code=None):
    """保存个股历史交易数据到mysql, 周线

    Args:
        last_stock_code: 最后一个股票的代码, 用来结束线程
    """
    logger.info('Begin save his data thread.')
    if last_stock_code:
        last_stock = last_stock_code
    else:
        last_stock = max_stock

    logger.info("Max stock code is: %s" % last_stock)

    while True:
        if his_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('his_data_queue\'s size is: %s' % (his_data_queue.qsize()))
            his_data = his_data_queue.get()
            code = his_data[0]
            ktype = his_data[1]
            data = his_data[2]
            logger.info('Get code: %s, ktype: %s from his_data_queue' % (code, ktype))
            data_dicts = [{'code': code, 'date': row[14],
                           'open': row[0], 'hign': row[1], 'close': row[2],
                           'low': row[3], 'volume': row[4],
                           'price_change': row[5], 'p_change':row[6],
                           'ma5':row[7], 'ma10': row[8], 'ma20': row[9],
                           'v_ma5': row[10], 'v_ma10': row[11],
                           'v_ma20': row[12], 'turnover': row[13]}
                          for row in data]
            try:
                # logger.info(data_dicts)
                # TODO: 添加5分钟, 15分钟.. 代码
                if ktype.upper() == 'D':
                    HistoryDataD.insert_many(data_dicts).execute()
                if ktype.upper() == 'W':
                    HistoryDataW.insert_many(data_dicts).execute()
                if ktype.upper() == 'M':
                    HistoryDataM.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Save data error. Code is %s, ktype is %s' % (code, ktype))
                logger.error(data)

            if code == last_stock:
                break


def save_his_data_scd():
    """保存个股历史交易数据到mysql, 分钟线"""
    logger.info('begin save his data scd thread.')
    while True:
        if his_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('his_data_scd_queue\'s size is: %s' % (his_data_scd_queue.qsize()))
            his_data = his_data_scd_queue.get()
            code = his_data[0]
            ktype = his_data[1]
            data = his_data[2]
            logger.info('get code: %s ktype: %s from his_data_scd_queue' % (code, ktype))
            data_dicts = [{'code': code, 'ktype': ktype, 'date': row[14],
                           'time': row[15], 'open': row[0], 'hign': row[1],
                           'close': row[2], 'low': row[3], 'volume': row[4],
                           'price_change': row[5], 'p_change':row[6],
                           'ma5':row[7], 'ma10': row[8], 'ma20': row[9],
                           'v_ma5': row[10], 'v_ma10': row[11],
                           'v_ma20': row[12], 'turnover': row[13]}
                          for row in data]
            # logger.info(data_dicts)
            HistoryDataScd.insert_many(data_dicts).execute()

            if code == max_stock:
                break


def get_his_data(code, start_date=None, end_date=None, ktype=None, retry_count=RETRY_COUNT, pause=PAUSE):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线数据。
    本接口只能获取近3年的日线数据，
    适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
    ktypes = list(['D', 'W', 'M'])

    def _deal_data(code, start, end, ktype, retry_count, pause):
        logger.info('Begin get data, code is: %s, start is: %s, end is: %s,ktype is: %s' % (code, start, end, ktype))
        try:
            data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
            if data_df is not None and not data_df.empty:
                data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
                data = data_df.values
                his_data_queue.put((code, ktype, data))
                logger.info('End get hist data: %s,%s,%s,%s' % (code, start, end, ktype))
            else:
                logger.info('Empty get hist data: %s,%s,%s,%s' % (code, start, end, ktype))

        except Exception as e:
            logger.exception('Get hist data error: %s,%s,%s,%s' % (code, start, end, ktype))

    if ktype is None:
        for ktype in ktypes:
            # threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
            _deal_data(code, start_date, end_date, ktype, retry_count, pause)
    else:
        # threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
        _deal_data(code, start_date, end_date, ktype, retry_count, pause)


def get_his_data_scd(code, start_date=None, end=None,
                     ktype=None, retry_count=RETRY_COUNT,
                     pause=PAUSE):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取5分钟、15分钟、30分钟和60分钟k线数据。
    本接口只能获取近3年的日线数据，
    适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
    ktypes = list(['5', '15', '30', '60'])

    def _deal_data(code, start, end, ktype, retry_count, pause):
        logger.info('Begin get hist data: %s,%s,%s' % (code, start, ktype))
        try:
            data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
            if data_df is not None and not data_df.empty:
                data_df['date'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[0]), index=data_df.index)
                data_df['time'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[1]), index=data_df.index)
                data = data_df.values
                his_data_scd_queue.put((code, ktype, data))
                logger.info('End get hist scd data: %s,%s,%s' % (code, start, ktype))
            else:
                logger.info('Empty get hist scd data: %s,%s,%s,%s' % (code, start, end, ktype))
        except Exception as e:
            logger.exception('Get data hist scd error:%s,%s,%s' % (code, start, ktype))

    if ktype is None:
        for ktype in ktypes:
            # threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
            _deal_data(code, start_date, end, ktype, retry_count, pause)
    else:
        # threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
        _deal_data(code, start_date, end, ktype, retry_count, pause)


def save_revote_his_data(code, start=None, end=None, autype='qfq',
                         index=True, retry_count=RETRY_COUNT, pause=PAUSE, drop_factor=True):
    """获取历史复权数据，分为前复权和后复权数据，接口提供股票上市以来所有历史数据，默认为前复权。如果不设定开始和结束日期，则返回近一年的复权数据，从性能上考虑，推荐设定开始日期和结束日期，而且最好不要超过三年以上，获取全部历史数据，请分年段分步获取，取到数据后，请及时在本地存储。

    本接口还提供大盘指数的全部历史数据，调用时，请务必设定index参数为True,由于大盘指数不存在复权的问题，故可以忽略autype参数。"""
    logger.info('Begin: %s,%s,%s' % (code, start, autype))
    try:
        data_df = ts.get_h_data(code, start, end, autype,
                                index, retry_count, pause, drop_factor)
        data_df['date'] = pd.Series(data_df.index, index=data_df.index)
        data = data_df.values
        data_dicts = [{'code': code, 'autype': autype, 'date': row[6], 'open': row[0], 'hign': row[1],
                       'close': row[2], 'low': row[3], 'volume': row[4], 'amount': row[5]} for row in data]
        RevoteHistoryData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('%s,%s' % (code, start))
    logger.info('End: %s,%s' % (code, start))


def save_today_all_data():
    """一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）"""
    logger.info('Begin get %s\'s all stock data.' % today)
    try:
        data_df = ts.get_today_all()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'date': today, 'changepercent': row[2], 'trade': row[3],
                       'open': row[4], 'hign': row[5], 'low': row[6], 'settlement': row[7], 'volume': row[8],
                       'turnoverratio': row[9], 'amount': row[10], 'per': row[11], 'pb': row[12],
                       'mktcap': row[13], 'nmc': row[14]} for row in data]
        TodayAllData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Get %s\'s all stock data.' % today)
    logger.info('End get %s\'s all stock data.' % today)


def save_tick_data(code=None, date=None, retry_count=RETRY_COUNT):
    """获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。
    
    在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame
      或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，
      当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取.

    当code为None,或者code长度不为6,或者date为None时直接返回None"""
    if code is None or date is None:
        logger.error('Get tick data. But code or date is None.')
        return
    logger.info('Begin get %s\'s tick data in %s.' % (code, date))
    try:
        data_df = ts.get_tick_data(code, date,retry_count)
        if data_df is not None and not data_df.empty:
            data = data_df.values
            data_dicts = [{'code': code, 'date': date, 'time': row[0], 'price': row[1], 'pchange': '',
                           'change': row[2], 'volume': row[3], 'amount': row[4], 'type': row[5]}
                          for row in data]
            TickData.insert_many(data_dicts).execute()
            logger.info('End get %s\'s tick data in %s.' % (code, date))
        else:
            logger.info('Empty get %s\'s tick data in %s.' % (code, date))
    except Exception as e:
        logger.exception('Error Get %s\'s tick data in %s.' % (code, date))


def get_tick_data(code, date, retry_count=RETRY_COUNT, pause=PAUSE, src='sn'):
    if code is None or date is None:
        logger.error('Get tick data. But code or date is None.')
        return
    logger.info('Begin get %s\'s tick data in %s.' % (code, date))
    try:
        data_df = ts.get_tick_data(code, date, retry_count)
        if data_df is not None and not data_df.empty:
            data = data_df.values
            tick_data_queue.put(code, data)
            logger.info('End get %s\'s tick data in %s.' % (code, date))
        else:
            logger.info('Empty get %s\'s tick data in %s.' % (code, date))
    except Exception as e:
        logger.exception('Error Get %s\'s tick data in %s.' % (code, date))


def save_big_index_data():
    """获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。"""
    logger.info('Begin get %s\'s big index data.' % today)
    try:
        data_df = ts.get_index()
        data = data_df.values
        data_dicts = [{'date': today, 'code': row[0], 'name': row[1], 'change': row[2], 'open': row[3],
                       'preclose': row[4], 'close': row[5], 'high': row[6], 'low': row[7],
                       'volume': row[8], 'amount': row[9]} for row in data]
        BigIndexData.insert_many(data_dicts).execute()
        logger.info('End get and save %s\'s big index data.' % today)
    except Exception as e:
        logger.exception('Error get and save %s\'s big index data.' % today)


def save_big_trade_data(code=None, date=None, vol=400, retry_count=RETRY_COUNT, pause=PAUSE):
    logger.info('Begin save %s\'s big trade data in %s.' % (code, date))
    try:
        data_df = ts.get_sina_dd(code, date, vol, retry_count, pause)
        data = data_df.values
        data_dicts = [{'date': date, 'code': row[0], 'name': row[1], 'time': row[2], 'price': row[3],
                       'volume': row[4], 'preprice': row[5], 'type': row[6]} for row in data]
        BigTradeData.insert_many(data_dicts).execute()
        logger.info('End save %s\'s big trade data in %s.' % (code, date))
    except Exception as e:
        logger.exception('Error save %s\'s big trade data in %s.' % (code, date))


def get_big_trade_data(code, date, vol=400, retry_count=RETRY_COUNT, pause=PAUSE):
    logger.info('Begin get %s\'s big trade data in %s.' % (code, date))
    try:
        data_df = ts.get_sina_dd(code, date, vol, retry_count, pause)
        if not data_df:
            logger.info('Empty get %s\'s big trade data in %s.' % (code, date))
        else:
            data = data_df.values
            big_trade_data_queue.put((code, date, data))
            logger.info('End get %s\'s big trade data in %s.' % (code, date))
    except Exception as e:
        logger.exception('Error get %s\'s big trade data in %s.' % (code, date))


def get_news(top=None, show_content=True):
    """获取即时财经新闻，类型包括国内财经、证券、外汇、期货、港股和美股等新闻信息。数据更新较快，使用过程中可用定时任务来获取。"""
    data_df = None
    logger.info('Begin get latest news.')
    try:
        data_df = ts.get_latest_news(top, show_content)
        now = str(get_time())
        logger.info('End get latest news.')
    except Exception as e:
        logger.exception('Error get latest news.')
    finally:
        return data_df


def get_news_time_and_url_in_mongo():
    db = mongo_utils.get_db()
    db_time_urls = db.news.find({}, {'time':1, 'url':1})
    time_urls = [(time_url['time'], time_url['url']) for time_url in db_time_urls]
    mongo_utils.close()
    return time_urls


def save_news2mongo(df):
    db = mongo_utils.get_db()
    news = json.loads(df.T.to_json()).values()
    db.news.insert(news)
    mongo_utils.close()


# if __name__ == '__main__':
# import sys
# print(sys.path())
# sys.path.append('/home/kay/WorkspacePython/stock_analysis')
# print(max_stock)