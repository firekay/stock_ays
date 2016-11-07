# encoding: UTF-8
import sys
import traceback
import logging
import logging.config
from peewee import *
import tushare as ts
import pandas as pd
from utils.mysql_utils import *
from utils.util import *
import threading
import time
from models.model import *
from queue import Queue

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()
today = get_today_line()

his_data_queue = Queue()
his_data_scd_queue = Queue()

@conn
def save_his_data():
    logger.info('begin save his data thread.')
    while(1):
        if his_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('his_data_queue\'s size is: %s' % (his_data_queue.qsize()))
            his_data = his_data_queue.get()
            code = his_data[0]
            ktype = his_data[1]
            data = his_data[2]
            logger.info('get code: %s, ktype: %s from his_data_queue' % (code, ktype))
            data_dicts = [ {'code': code, 'ktype': ktype, 'date': row[14], 
                'open': row[0], 'hign': row[1], 'close': row[2], 
                'low': row[3], 'volume': row[4], 
                'price_change': row[5], 'p_change':row[6], 
                'ma5':row[7], 'ma10': row[8], 'ma20': row[9],
                'v_ma5': row[10], 'v_ma10': row[11], 
                'v_ma20': row[12], 'turnover': row[13]} 
                for row in data ]
            logger.info(data_dicts)
            HistoryData.insert_many(data_dicts).execute()
            
            if code == get_max_stock():
                break


@conn
def save_his_data_scd():
    logger.info('begin save his data_scd thread.')
    while(1):
        if his_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('his_data_scd_queue\'s size is: %s' % (his_data_scd_queue.qsize()))
            his_data = his_data_scd_queue.get()
            code = his_data[0]
            ktype = his_data[1]
            data = his_data[2]
            logger.info('get code: %s ktype: %s from his_data_scd_queue' % (code, ktype))
            data_dicts = [ {'code': code, 'ktype': ktype, 'date': row[14], 
                            'time': row[15], 'open': row[0], 'hign': row[1],
                            'close': row[2], 'low': row[3], 'volume': row[4], 
                            'price_change': row[5], 'p_change':row[6], 
                            'ma5':row[7], 'ma10': row[8], 'ma20': row[9],
                            'v_ma5': row[10], 'v_ma10': row[11], 
                            'v_ma20': row[12], 'turnover': row[13]} 
                           for row in data ]
            logger.info(data_dicts)
            HistoryDataScd.insert_many(data_dicts).execute()
            
            if code == get_max_stock():
                break

@conn
def get_max_stock():
    """获取股票列表"""
    stocks = StockBasic.select(StockBasic.code).order_by(StockBasic.code.desc()).limit(1)
    max_sotck = [stock.code for stock in stocks][0]
    return max_sotck


@conn
def get_stocks():
    """获取股票列表"""
    return StockBasic.select(StockBasic.code).order_by(StockBasic.code)


def get_his_data(code, start=None, end=None,
                  ktype=None, retry_count=10,
                  pause=0.001):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线数据。
    本接口只能获取近3年的日线数据，
    适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
    ktypes = list(['D','W', 'M'])
    def _deal_data(code, start, end, ktype, retry_count, pause):
        logger.info('Begin get data: %s,%s,%s' % (code, start, ktype))
        print('Begin get data: %s,%s,%s' % (code, start, ktype))
        try:
            data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
            if not data_df.empty:
                data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
                data = data_df.values
                his_data_queue.put((code, ktype, data))
                logger.info('End get data: %s,%s,%s' % (code, start, ktype))
                print('End get data: %s,%s,%s' % (code, start, ktype))
            else:
                logger.info('Empty get data: %s,%s,%s,%s' % (code, start, end, ktype))

        except Exception as e:
            logger.error('Get data error: %s,%s,%s' % (code, start, ktype))
            logger.error(traceback.format_exc())
            print('%s,%s,%s' % (code, start, ktype))
            print(traceback.format_exc())
        logger.info('End get data: %s,%s,%s' % (code, start, ktype))
        print('End get data: %s,%s,%s' % (code, start, ktype))

    if ktype is None:
        for ktype in ktypes:
            threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
            #_deal_data(code, start, end, ktype, retry_count, pause)
    else:
        threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
        #_deal_data(code, start, end, ktype, retry_count, pause))


def get_his_data_scd(code, start=None, end=None,
                  ktype=None, retry_count=10,
                  pause=0.001):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取5分钟、15分钟、30分钟和60分钟k线数据。
    本接口只能获取近3年的日线数据，
    适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
    ktypes = list(['5', '15', '30', '60'])
    def deal_data(code, start, end, ktype, retry_count, pause):
        logger.info('Begin get data: %s,%s,%s' % (code, start, ktype))
        print('Begin get data: %s,%s,%s' % (code, start, ktype))
        try:
            data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
            if not data_df.empty:
                data_df['date'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[0]), index=data_df.index)
                data_df['time'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[1]), index=data_df.index)
                data = data_df.values
                his_data_scd_queue.put((code, ktype, data))
                logger.info('End get data: %s,%s,%s' % (code, start, ktype))
                print('End get data: %s,%s,%s' % (code, start, ktype))
            else:
                logger.info('Empty get data: %s,%s,%s,%s' % (code, start, end, ktype))
        except Exception as e:
            logger.error('Get data error:%s,%s,%s' % (code, start, ktype))
            logger.error(traceback.format_exc())
            print('Get data error:%s,%s,%s' % (code, start, ktype))
            print(traceback.format_exc())

    if ktype is None:
        for ktype in ktypes:
            deal_data(code, start, end, ktype, retry_count, pause)
    else:
        deal_data(code, start, end, ktype, retry_count, pause)

# @conn
# def save_his_data(code, start=None, end=None,
#                   ktype=None, retry_count=10,
#                   pause=0.001):
#     """获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线数据。
#     本接口只能获取近3年的日线数据，
#     适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
#     ktypes = list(['D','W', 'M'])
#     def _deal_data(code, start, end, ktype, retry_count, pause):
#         logger.info('Begin: %s,%s,%s' % (code, start, ktype))
#         print('Begin: %s,%s,%s' % (code, start, ktype))
#         try:
#             data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
#             data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
#             data = data_df.values
#             data_dicts = [ {'code': code, 'ktype': ktype, 'date': row[14], 
#                             'open': row[0], 'hign': row[1], 'close': row[2], 
#                             'low': row[3], 'volume': row[4], 
#                             'price_change': row[5], 'p_change':row[6], 
#                             'ma5':row[7], 'ma10': row[8], 'ma20': row[9],
#                             'v_ma5': row[10], 'v_ma10': row[11], 
#                             'v_ma20': row[12], 'turnover': row[13]} 
#                            for row in data ]
#             HistoryData.insert_many(data_dicts).execute()
#         except Exception as e:
#             logger.error('%s,%s,%s' % (code, start, ktype))
#             logger.error(traceback.format_exc())
#             print('%s,%s,%s' % (code, start, ktype))
#             print(traceback.format_exc())
#         logger.info('End: %s,%s,%s' % (code, start, ktype))
#         print('End: %s,%s,%s' % (code, start, ktype))

#     if ktype is None:
#         for ktype in ktypes:
#             threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
#             #_deal_data(code, start, end, ktype, retry_count, pause)
#     else:
#         threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
#         #_deal_data(code, start, end, ktype, retry_count, pause)


# @conn
# def save_his_data_scd(code, start=None, end=None,
#                   ktype=None, retry_count=10,
#                   pause=0.001):
#     """获取个股历史交易数据（包括均线数据），可以通过参数设置获取5分钟、15分钟、30分钟和60分钟k线数据。
#     本接口只能获取近3年的日线数据，
#     适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
#     ktypes = list(['5', '15', '30', '60'])
#     def deal_data(code, start, end, ktype, retry_count, pause):
#         logger.info('Begin: %s,%s,%s' % (code, start, ktype))
#         print('Begin: %s,%s,%s' % (code, start, ktype))
#         try:
#             data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
#             data_df['date'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[0]), index=data_df.index)
#             data_df['time'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[1]), index=data_df.index)
#             data = data_df.values
#             data_dicts = [ {'code': code, 'ktype': ktype, 'date': row[14], 'time': row[15], 'open': row[0], 'hign': row[1], 'close': row[2], 'low': row[3], 'volume': row[4], 'price_change': row[5], 'p_change':row[6], 'ma5':row[7], 'ma10': row[8], 'ma20': row[9], 'v_ma5': row[10], 'v_ma10': row[11], 'v_ma20': row[12], 'turnover': row[13]} for row in data ]
#             HistoryDataScd.insert_many(data_dicts).execute()
#         except Exception as e:
#             logger.error('%s,%s,%s' % (code, start, ktype))
#             logger.error(traceback.format_exc())
#             print('%s,%s,%s' % (code, start, ktype))
#             print(traceback.format_exc())
#         logger.info('End: %s,%s,%s' % (code, start, ktype))
#         print('End: %s,%s,%s' % (code, start, ktype))

#     if ktype is None:
#         for ktype in ktypes:
#             deal_data(code, start, end, ktype, retry_count, pause)
#     else:
#         deal_data(code, start, end, ktype, retry_count, pause)


def save_revote_his_data(code, start=None, end=None, autype='qfq',
               index=True, retry_count=10, pause=0.001, drop_factor=True):
    """获取历史复权数据，分为前复权和后复权数据，接口提供股票上市以来所有历史数据，默认为前复权。如果不设定开始和结束日期，则返回近一年的复权数据，从性能上考虑，推荐设定开始日期和结束日期，而且最好不要超过三年以上，获取全部历史数据，请分年段分步获取，取到数据后，请及时在本地存储。

    本接口还提供大盘指数的全部历史数据，调用时，请务必设定index参数为True,由于大盘指数不存在复权的问题，故可以忽略autype参数。"""
    logger.info('Begin: %s,%s,%s' % (code, start, autype))
    print('Begin: %s,%s,%s' % (code, start, autype))
    try:
        data_df = ts.get_h_data(code, start, end, autype,
               index, retry_count, pause, drop_facto)
        data_df['date'] = pd.Series(data_df.index, index=data_df.index)
        data = data_df.values
        data_dicts = [ {'code': code, 'autype': autype, 'date': row[6], 'open': row[0], 'hign': row[1], 'close': row[2], 'low': row[3], 'volume': row[4], 'amount': row[5]} for row in data ]
        RevoteHistoryData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('%s,%s,%s' % (code, start, ktype))
        logger.error(traceback.format_exc())
        print('%s,%s,%s' % (code, start, ktype))
        print(traceback.format_exc())
    logger.info('End: %s,%s,%s' % (code, start, ktype))
    print('End: %s,%s,%s' % (code, start, ktype))


def save_today_all_data():
    """一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）"""
    today = get_today_line()
    logger.info('Begin get %s\'s all stock data.' % (today))
    print('Begin get %s\'s all stock data.' % (today))
    try:
        data_df = ts.get_today_all()
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'date': today, 'changepercent': row[2], 'trade': row[3], 'open': row[4], 'hign': row[5], 'low': row[6], 'settlement': row[7], 'volume': row[8], 'turnoverratio': row[9], 'amount': row[10], 'per': row[11], 'mktcap': row[12], 'nmc': row[13]} for row in data ]
        TodayAllData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get %s\'s all stock data.' % (today))
        logger.error(traceback.format_exc())
        print('Get %s\'s all stock data.' % (today))
        print(traceback.format_exc())
    logger.info('End get %s\'s all stock data.' % (today))
    print('End get %s\'s all stock data.' % (today))


def save_tick_data(code=None, date=None, retry_count=10):
    """获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取.

    当code为None,或者code长度不为6,或者date为None时直接返回None"""
    if code is None or date is None:
        logger.error('Get tick data. But code or date is None.' % (code, date))
        return None
    logger.info('Begin get %s\'s tick data in %s.' % (code, date))
    try:
        data_df = ts.get_tick_data(code, date,retry_count)
        data = data_df.values
        data_dicts = [ {'code': code, 'date': date, 'time': row[0], 'price': row[1], 'pchange': '', 'change': row[2], 'volume': row[3], 'amount': row[4], 'type': row[5]} for row in data ]
        TickData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get %s\'s tick data in %s.' % (code, date))
        logger.error(traceback.format_exc())
        print(traceback.format_exc())
    logger.info('End get %s\'s tick data in %s.' % (code, date))
    print('End. %s ' % (today))


def save_big_index_data():
    """获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。"""
    logger.info('Begin get %s\'s big index data.' % (today))
    try:
        data_df = ts.get_index()
        data = data_df.values
        data_dicts = [ {'date': today, 'code': row[0], 'name': row[1], 'change': row[2], 'open': row[3], 'preclose': row[4], 'close': row[5], 'high': row[6], 'low': row[7], 'volume': row[8], 'amount': row[9]} for row in data ]
        BigIndexData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get %s\'s big index data.' % (today))
        logger.error(traceback.format_exc())
        print('Get %s\'s big index data.' % (today))
        print(traceback.format_exc())
    logger.info('End get %s\'s big index data.' % (today))
    print('End get %s\'s big index data.' % (today))


def save_big_trade_data(code=None, date=None, vol=400, retry_count=10, pause=0.001):
    logger.info('Begin get %s\'s big trade data in %s.' % (code, date))
    try:
        data_df = ts.get_sina_dd(code, date, vol, retry_count, pause)
        data = data_df.values
        data_dicts = [ {'date': date, 'code': row[0], 'name': row[1], 'time': row[2], 'price': row[3], 'volume': row[4], 'preprice': row[5], 'type': row[6]} for row in data ]
        BigTradeData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get %s\'s big trade data in %s.' % (code, date))
        logger.error(traceback.format_exc())
        print('Get %s\'s big trade data in %s.' % (code, date))
        print(traceback.format_exc())
    logger.info('End get %s\'s big trade data in %s.' % (code, date))
    print('End get %s\'s big trade data in %s.' % (code, date))


def save_industry_classified():
    '''在现实交易中，经常会按行业统计股票的涨跌幅或资金进出，本接口按照sina财经对沪深股票进行的行业分类，返回所有股票所属行业的信息。'''
    logger.info('Begin get industry classified行业信息.')
    try:
        data_df = ts.get_industry_classified(standard=type)
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
        IndustryClassified.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get industry classified行业信息.')
        logger.error(traceback.format_exc())
    logger.info('End get industry classified行业信息.')



def save_concept_classified():
    """返回股票概念的分类数据，现实的二级市场交易中，经常会以”概念”来炒作，在数据分析过程中，可根据概念分类监测资金等信息的变动情况。"""
    logger.info('Begin get concept clssified股票概念的分类数据.')
    try:
        data_df = ts.get_concept_classified()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
        ConceptClassified.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get concept clssified股票概念的分类数据.')
        logger.error(traceback.format_exc())
    logger.info('End get concept clssified股票概念的分类数据.')


def save_area_classified():
    """按地域对股票进行分类，即查找出哪些股票属于哪个省份。"""
    logger.info('Begin get area clssified.')
    try:
        data_df = ts.get_area_classified()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'area': row[2]} for row in data ]
        AreaClassified.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get area clssified.')
        logger.error(traceback.format_exc())
    logger.info('End get area clssified.')
    

def save_sme_classified():
    """获取中小板股票数据，即查找所有002开头的股票"""
    logger.info('Begin get sme中小板 clssified.')
    try:
        data_df = ts.get_sme_classified()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
        SmeClassified.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get sme中小板 classified.')
        logger.error(traceback.format_exc())
    logger.info('End get sme中小板 classified.')


def save_gem_classified():
    """获取创业板股票数据，即查找所有300开头的股票"""
    logger.info('Begin get gem 创业板股票数据clssified.')
    try:
        data_df = ts.get_gem_classified()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
        GemClassified.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get gem 创业板股票数据classified.')
        logger.error(traceback.format_exc())
    logger.info('End get gem 创业板股票数据classified.')


def save_st_classified():
    """获取风险警示板股票数据，即查找所有st股票"""
    logger.info('Begin get st clssified.')
    try:
        data_df = ts.get_st_classified()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
        StClassified.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get st classified.')
        logger.error(traceback.format_exc())
    logger.info('End get st classified.')


def save_hs300s():
    """获取沪深300当前成份股及所占权重"""
    logger.info('Begin get hs300 clssified.')
    try:
        data_df = ts.get_hs300s()
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'date': row[2], 'weight': row[3]} for row in data ]
        Hs300.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get hs300 classified.')
        logger.error(traceback.format_exc())
    logger.info('End get hs300 classified.')


def save_sz50s():
    """上证50成分股"""
    logger.info('Begin get sz50 clssified.')
    try:
        data_df = ts.get_sz50s()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
        Sz50.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get sz50 classified.')
        logger.error(traceback.format_exc())
    logger.info('End get sz50 classified.')


def save_zz500s():
    """中证500成分股"""
    logger.info('Begin get zz500 clssified.')
    try:
        data_df = ts.get_zz500s()    
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
        Zz500.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get zz500 classified.')
        logger.error(traceback.format_exc())
    logger.info('End get zz500 classified.')


def save_terminated():
    """获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    logger.info('Begin get terminated clssified.')
    try:
        today = str(get_today())
        data_df = ts.get_terminated()
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'o_date': row[2], 't_date': row[3], 'insert_date': today} for row in data ]
        Terminated.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get terminated classified.')
        logger.error(traceback.format_exc())
    logger.info('End get terminated classified.')


def save_suspend():
    """获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    logger.info('Begin get suspend clssified.')
    try:
        today = str(get_today())
        data_df = ts.get_terminated()
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'o_date': row[2], 't_date': row[3], 'insert_date': today} for row in data ]
        Suspend.insert_many(data_dicts).execute()
    except Exception as e:
        logger.error('Get suspend classified.')
        logger.error(traceback.format_exc())
    logger.info('End get suspend classified.')



def truncate_table(cls):
    """清空表
    
    参数为model中的类名。
    """
    print(cls)
    cls.truncate_table()


def create_table(cls):
    """创建表。

    参数为model中的类名
    """
    cls.create_table()


# if __name__ == '__main__':
    # import sys
    # print(sys.path())
    # sys.path.append('/home/kay/WorkspacePython/stock_analysis')
    # print(get_max_stock())
