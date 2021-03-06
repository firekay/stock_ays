# encoding: UTF-8
"""调用接口得到数据，以及存入mysql， mongodb

get 为从外部tushare获取数据
load 为从mysql获取数据
"""
import logging
import tushare as ts
import pandas as pd
from queue import Queue
import json
import time
from dal.constants import *
from utils import mongo_utils
from models.model import *

logger = logging.getLogger(__name__)
today_line = get_today_line()

his_data_queue = Queue()
h_revote_data_queue = Queue()
stock_k_data_queue = Queue()
tick_data_queue = Queue()
today_tick_data_queue = Queue()
big_trade_data_queue = Queue()


########################################################
# stock k data
########################################################
def get_stock_k_data(code, start_date=None, end_date=None, autype='qfq', index=False,
                     ktype=None, retry_count=RETRY_COUNT, pause=PAUSE):
    """获取k线数据的历史复权数据
    
    新接口融合了get_hist_data和get_h_data两个接口的功能，即能方便获取日周月的低频数据，
    也可以获取5、15、30和60分钟相对高频的数据。
    同时，上市以来的前后复权数据也能在一行代码中轻松获得，当然，您也可以选择不复权。
    
    Args:
        code: 股票代码 e.g. '600848'
        start_date:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
        end_date:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
        autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
        index:Boolean，是否是大盘指数，默认为False
        ktype: 数据类型: D, W M, 默认为D
        retry_count: 重试次数
        pause: 重试间隔
    """
    def filter_start_and_end(obj):
        date_str = str(obj).split(' ')[0]
        return start_date <= date_str <= end_date

    if ktype is None:
        ktype = 'D'
    ktypes = ['D', 'W', 'M', '5', '15', '30', '60']
    assert ktype in ktypes, 'ktype must be one of %s' % ktypes
    if start_date is not None or end_date is not None:
        logger.info('Begin get stock %s history k data, start date is: %s, end date is: %s, ktype is %s.'
                    % (code, start_date, end_date, ktype))
    else:
        logger.info('Begin get stock %s history k data, all date, ktype is %s.' % (code, ktype))
    # get_k_data must transmit '' not None
    if start_date is None:
        start_date = ''
    if end_date is None:
        end_date = ''
    try:
        data_df = ts.get_k_data(code, start=start_date, end=end_date, ktype=ktype, index=index,
                                retry_count=retry_count, pause=pause)
    except IOError:
        logger.exception('Error get stock k data, sleep 1m, then try again. code is: %s.' % code)
        time.sleep(1 * 60)
        get_stock_k_data(code, start_date, end_date, autype, index, ktype,retry_count, pause)
    except Exception as e:
        if start_date != '' or end_date != '':
            logger.exception('Error get stock %s history k data, start date is: %s, end date is: %s, ktype is: %s.'
                             % (code, start_date, end_date, ktype))
        else:
            logger.exception('Error get stock %s history k data, all date, ktype is: %s.' % (code, ktype))
    else:
        if data_df is not None and not data_df.empty:
            # data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
            # get one day data with result lots of days data, so filter only have between start_date and end_data.
            if start_date != '':
                data_df = data_df[data_df.date.map(lambda d: filter_start_and_end(d))]
                if data_df is not None and not data_df.empty:
                    data = data_df.values
                    stock_k_data_queue.put((code, ktype, autype, data))
                    logger.info('Success get stock %s history k data, start date is: %s, end date is: %s, ktype is: %s.'
                                % (code, start_date, end_date, ktype))
                else:
                    logger.warn('Empty get stock %s history k data, start date is: %s, end date is: %s, ktype is %s.'
                                % (code, start_date, end_date, ktype))

            else:
                data = data_df.values
                stock_k_data_queue.put((code, ktype, autype, data))
                logger.info('Success get stock %s history k data, all date, ktype is %s.' % (code, ktype))
        else:
            if start_date != '' or end_date != '':
                logger.warn('Empty get stock %s history k data, start date is: %s, end date is: %s, ktype is %s.'
                            % (code, start_date, end_date, ktype))
            else:
                logger.info('Empty get stock %s history k data, all date, ktype is: %s.' % (code, ktype))


def save_stock_k_data():
    """保存k线数据的历史复权数据"""
    logger.info('Begin save stock k data thread.')
    while True:
        if stock_k_data_queue.empty():
            time.sleep(0.01)
        else:
            stock_k_data = stock_k_data_queue.get()
            logger.info('stock_k_data_queue\'s size is: %s' % (stock_k_data_queue.qsize()))
            code = stock_k_data[0]
            ktype = stock_k_data[1]
            # when ktype is stop, stop the thread
            if ktype == 'stop':
                logger.info('Stop save stock k data thread.')
                break
            autype = stock_k_data[2]
            data = stock_k_data[3]
            logger.info('Get stock k data from stock_k_data_queue, stock code is: %s, ktype is: %s.' %
                        (code, ktype))
            data_dicts = [{'code': code, 'autype': autype, 'date': row[0], 'open':row[1],
                           'close': row[2], 'high': row[3], 'low': row[4], 'volume': row[5]} for row in data]
            logging.info('Begin save stock k data, code is: %s, ktype is %s.' % (code, ktype))

            try:
                if ktype.upper() == 'D':
                    HistoryKDataD.insert_many(data_dicts).execute()
                elif ktype.upper() == 'W':
                    HistoryKDataW.insert_many(data_dicts).execute()
                elif ktype.upper() == 'M':
                    HistoryKDataM.insert_many(data_dicts).execute()
                elif ktype == '5':
                    HistoryKData5.insert_many(data_dicts).execute()
                elif ktype == '15':
                    HistoryKData15.insert_many(data_dicts).execute()
                elif ktype == '30':
                    HistoryKData30.insert_many(data_dicts).execute()
                elif ktype == '60':
                    HistoryKData60.insert_many(data_dicts).execute()
                else:
                    pass
            except Exception as e:
                logger.exception('Error save stock k data, code is: %s, ktype is: %s.' % (code, ktype))
                logger.error('Error data is: %s' % data)
            else:
                logging.info('Success save stock k data, code is: %s, ktype is %s.' % (code, ktype))


def load_stock_k_data(model_ktype, stock=None, start_date=None, end_date=None):
    """load stock k data from mysql
    
    Args:
        model_ktype: string, 可选值'D', 'W', 'M', '5', '15', '30', '60'
        stock: string, 股票代码
        start_date: string, 开始时间
        end_date: string, 结束时间
    """
    model_ktypes = ['D', 'W', 'M', '5', '15', '30', '60']
    assert model_ktype in model_ktypes, 'model_ktype must be one of %s' % model_ktypes
    model = HistoryKDataD
    if model_ktype.upper() == 'D':
        model = HistoryKDataD
    elif model_ktype.upper() == 'W':
        model = HistoryKDataW
    elif model_ktype.upper() == 'M':
        model = HistoryKDataM
    elif model_ktype == '5':
        model = HistoryKData5
    elif model_ktype == '15':
        model = HistoryKData15
    elif model_ktype == '30':
        model = HistoryKData30
    elif model_ktype == '60':
        model = HistoryKData60
    else:
        pass

    if stock:
        if start_date:
            if end_date:
                get_stocks = model.select().where(model.code == stock, model.date >= start_date,
                                                  model.date <= end_date) \
                    .order_by(model.date)
            else:
                get_stocks = model.select().where(model.code == stock, model.date >= start_date) \
                    .order_by(model.date)
        else:
            if end_date:
                get_stocks = model.select().where(model.code == stock, model.date <= end_date) \
                    .order_by(model.date)
            else:
                get_stocks = model.select().where(model.code == stock) \
                    .order_by(model.date)
    else:
        if start_date:
            if end_date:
                get_stocks = model.select().where(model.date >= start_date, model.date <= end_date)\
                    .order_by(model.code, model.date)
            else:
                get_stocks = model.select().where(model.date >= start_date) \
                    .order_by(model.code, model.date)
        else:
            if end_date:
                get_stocks = model.select().where(model.date <= end_date) \
                    .order_by(model.code, model.date)
            else:
                get_stocks = model.select().order_by(model.code, model.date)
    return get_stocks


########################################################
# h revote data
########################################################
def save_h_revote_data():
    logger.info('Begin save h revote data thread.')
    while True:
        if h_revote_data_queue.empty():
            time.sleep(0.01)
        else:
            logger.info('h_revote_data_queue\'s size is: %s' % (his_data_queue.qsize()))
            h_revote_data = h_revote_data_queue.get()
            code = h_revote_data[0]
            autype = h_revote_data[1]
            # when autype is stop, stop the thread
            if autype == 'stop':
                logger.info('Stop save h revote data thread.')
                break
            data = h_revote_data[2]
            logger.info('Get h revode data from h_revote_data_queue, stock code is: %s.' % code)
            data_dicts = [{'code': code, 'autype': autype, 'date': row[6], 'open': row[0], 'high': row[1],
                           'close': row[2], 'low': row[3], 'volume': row[4], 'amount': row[5]} for row in data]
            logger.info('Begin save history revote data, stock is: %s.' % code)
            try:
                RevoteHistoryData.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Error save history revote data, stock is: %s.' % code)
                logger.error('Error data is: %s.' % data)
            else:
                logger.info('Success save history revote data, stock is: %s.' % code)


def get_h_revote_data(code, start_date=None, end_date=None, autype='qfp', index=False,
                      retry_count=RETRY_COUNT, pause=0, drop_factor=True):
    if start_date is not None or end_date is not None:
        logger.info('Begin get stock h revote data, code is: %s, start date is: %s, end date is: %s.'
                    % (code, start_date, end_date))
    else:
        logger.info('Begin get stock h revote data, all date, code is: %s.' % code)

    try:
        data_df = ts.get_h_data(code, start_date, end_date, autype,
                                index, retry_count, pause, drop_factor)
    except IOError:
        logger.exception('Error get stock h revote data, sleep 5m, then try again. code is: %s.' % code)
        time.sleep(5 * 60)
        get_h_revote_data(code, start_date, end_date, autype, index, retry_count, pause, drop_factor)
    except Exception as e:
        if start_date is not None or end_date is not None:
            logger.exception('Error get stock h revote data, code is: %s start date is: %s, end date is: %s.'
                             % (code, start_date, end_date))
        else:
            logger.exception('Error get stock h revote data, all date, the code is: %s.' % code)
    else:
        if data_df is not None and not data_df.empty:
            data_df['date'] = pd.Series(data_df.index, index=data_df.index)
            data_df['date'] = data_df['date'].astype(str)
            data = data_df.values
            h_revote_data_queue.put((code, autype, data))
            if start_date is not None or end_date is not None:
                logger.info('Success get stock h revote data, code is: %s, start date is: %s, end date is: %s.'
                            % (code, start_date, end_date))
            else:
                logger.info('Success get stock h revote data, all date, code is: %s.' % code)
        else:
            if start_date is not None or end_date is not None:
                logger.warn('Empty get stock h revote data, code is: %s, start date is: %s, end date is: %s.'
                            % (code, start_date, end_date))
            else:
                logger.warn('Empty get stock h revote data, all date, code is: %s.' % code)


########################################################
# his data
########################################################
def save_his_data():
    """保存个股历史交易数据到mysql, 周线
    """
    logger.info('Begin save his data thread.')
    while True:
        if his_data_queue.empty():
            time.sleep(0.01)
        else:
            his_data = his_data_queue.get()
            logger.info('his_data_queue\'s size is: %s' % (his_data_queue.qsize()))
            code = his_data[0]
            ktype = his_data[1]
            if ktype == 'stop':
                logger.info('Stop save his data thread.')
                break
            data = his_data[2]
            logger.info('Get history data from his_data_queue, code: %s, ktype: %s.' % (code, ktype))
            data_dicts = [{'code': code, 'date': row[14],
                           'open': row[0], 'high': row[1], 'close': row[2],
                           'low': row[3], 'volume': row[4],
                           'price_change': row[5], 'p_change':row[6],
                           'ma5':row[7], 'ma10': row[8], 'ma20': row[9],
                           'v_ma5': row[10], 'v_ma10': row[11],
                           'v_ma20': row[12], 'turnover': row[13]}
                          for row in data]
            logger.info('Begin save history data from his_data_queue, code: %s, ktype: %s.' % (code, ktype))
            try:
                if ktype.upper() == 'D':
                    HistoryDataD.insert_many(data_dicts).execute()
                if ktype.upper() == 'W':
                    HistoryDataW.insert_many(data_dicts).execute()
                if ktype.upper() == 'M':
                    HistoryDataM.insert_many(data_dicts).execute()
                elif ktype == '5':
                    HistoryData5.insert_many(data_dicts).execute()
                elif ktype == '15':
                    HistoryData15.insert_many(data_dicts).execute()
                elif ktype == '30':
                    HistoryData30.insert_many(data_dicts).execute()
                elif ktype == '60':
                    HistoryData60.insert_many(data_dicts).execute()
                else:
                    pass
            except Exception as e:
                logger.exception('Error save history data from his_data_queue, code: %s, ktype: %s.' % (code, ktype))
                logger.error('Error data is: %s' % data)
            else:
                logger.info('Success save history data from his_data_queue, code: %s, ktype: %s.' % (code, ktype))


def get_his_data(code, start_date=None, end_date=None, ktype=None, retry_count=RETRY_COUNT, pause=PAUSE):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线数据。
    本接口只能获取近3年的日线数据，
    适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
    if ktype is None:
        ktype = 'D'
    ktypes = ['D', 'W', 'M', '5', '15', '30', '60']
    assert ktype in ktypes, 'ktype must be one of %s' % ktypes
    if start_date is not None:
        logger.info('Begin get data, code is: %s, start_date is: %s, end_date is: %s,ktype is: %s'
                    % (code, start_date, end_date, ktype))
    else:
        logger.info('Begin get data, all date, code is: %s, ktype is: %s'
                    % (code, ktype))
    try:
        data_df = ts.get_hist_data(code=code, start=start_date, end=end_date, ktype=ktype,
                                   retry_count=retry_count, pause=pause)
    except IOError:
        logger.exception('Error get stock history data, sleep 1m, then try again. code is: %s.' % code)
        time.sleep(1 * 60)
        get_his_data(code, start_date, end_date, ktype, retry_count, pause)
    except Exception as e:
        if start_date is not None:
            logger.exception('Error get data, code is: %s, start_date is: %s, end_date is: %s,ktype is: %s'
                             % (code, start_date, end_date, ktype))
        else:
            logger.exception('Error get data, all date, code is: %s, ktype is: %s'
                             % (code, ktype))
    else:
        if data_df.empty:
            if start_date is not None:
                logger.warn('Empty get data, code is: %s, start_date is: %s, end_date is: %s,ktype is: %s'
                            % (code, start_date, end_date, ktype))
            else:
                logger.warn('Empty get data, all date, code is: %s, ktype is: %s'
                            % (code, ktype))
        else:
            data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
            data = data_df.values
            his_data_queue.put((code, ktype, data))
            if start_date is not None:
                logger.info('Success get data, code is: %s, start_date is: %s, end_date is: %s,ktype is: %s'
                            % (code, start_date, end_date, ktype))
            else:
                logger.info('Success get data, all date, code is: %s, ktype is: %s'
                            % (code, ktype))


# def get_his_data_scd(code, start_date=None, end=None,
#                      ktype=None, retry_count=RETRY_COUNT,
#                      pause=PAUSE):
#     """获取个股历史交易数据（包括均线数据），可以通过参数设置获取5分钟、15分钟、30分钟和60分钟k线数据。
#     本接口只能获取近3年的日线数据，
#     适合搭配均线数据进行选股和分析，如果需要全部历史数据，请调用下一个接口get_h_data()。"""
#     ktypes = list(['5', '15', '30', '60'])
#
#     def _deal_data(code, start, end, ktype, retry_count, pause):
#         logger.info('Begin get hist data: %s,%s,%s' % (code, start, ktype))
#         try:
#             data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
#             if data_df is not None and not data_df.empty:
#                 data_df['date'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[0]), index=data_df.index)
#                 data_df['time'] = pd.Series(data_df.index.map(lambda s: s.split(' ')[1]), index=data_df.index)
#                 data = data_df.values
#                 his_data_scd_queue.put((code, ktype, data))
#                 logger.info('End get hist scd data: %s,%s,%s' % (code, start, ktype))
#             else:
#                 logger.info('Empty get hist scd data: %s,%s,%s,%s' % (code, start, end, ktype))
#         except Exception as e:
#             logger.exception('Get data hist scd error:%s,%s,%s' % (code, start, ktype))
#
#     if ktype is None:
#         for ktype in ktypes:
#             # threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
#             _deal_data(code, start_date, end, ktype, retry_count, pause)
#     else:
#         # threading.Thread(target=_deal_data, args=(code, start, end, ktype, retry_count, pause)).start()
#         _deal_data(code, start_date, end, ktype, retry_count, pause)
#

########################################################
# revote his data
########################################################
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
        data_dicts = [{'code': code, 'autype': autype, 'date': row[6], 'open': row[0], 'high': row[1],
                       'close': row[2], 'low': row[3], 'volume': row[4], 'amount': row[5]} for row in data]
        RevoteHistoryData.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('%s,%s' % (code, start))
    logger.info('End: %s,%s' % (code, start))


########################################################
#  today all data
########################################################
def save_today_all_data():
    """一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）"""
    logger.info('Begin get and save today all stock data, the date is: %s' % today_line)
    try:
        data_df = ts.get_today_all()
    except Exception as e:
        logger.exception('Error get today all stock data, the date is: %s' % today_line)
    else:
        if data_df is not None and not data_df.empty:
            data = data_df.values
            data_dicts = [{'code': row[0], 'name': row[1], 'date': today_line, 'changepercent': row[2], 'trade': row[3],
                           'open': row[4], 'high': row[5], 'low': row[6], 'settlement': row[7], 'volume': row[8],
                           'turnoverratio': row[9], 'amount': row[10], 'per': row[11], 'pb': row[12],
                           'mktcap': row[13], 'nmc': row[14]} for row in data]
            try:
                TodayAllData.insert_many(data_dicts).execute()
            except IOError:
                logger.exception('Error get today all data, sleep 5m, then try again.')
                time.sleep(10)
                save_today_all_data()
            except Exception:
                logger.exception('Error save today all stock data, the date is: %s' % today_line)
                logger.error('Error data is: %s' % data)
            else:
                logger.info('Success get and save today all stock data, the date is: %s' % today_line)
        else:
            logger.warn('Empty get and save today all stock data, the date is: %s' % today_line)


########################################################
#  tick data
########################################################
def save_tick_data():
    """获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。
    
    在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame
      或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，
      当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取.
    """
    logger.info('Begin save tick data thread.')

    while True:
        if tick_data_queue.empty():
            time.sleep(0.01)
        else:
            tick_data = tick_data_queue.get()
            logger.info('tick_data_queue\'s size is: %s' % tick_data_queue.qsize())
            code = tick_data[0]
            date = tick_data[1]
            data = tick_data[2]
            # when date is stop, stop this thread. (control in transaction_service)
            if date == 'stop':
                logger.info('Last tick data stock code is: %s.' % code)
                logger.info('Stop save tick data thread.')
                break
            logger.info('Get tick data from tick_data_queue, stock code is: %s, data is: %s'
                        % (code, date))
            data_dicts = [{'code': code, 'date': date, 'time': row[0], 'price': row[1], 'pchange': '',
                           'change': row[2], 'volume': row[3], 'amount': row[4], 'type': row[5]}
                          for row in data]
            logger.info('Begin save tick data, code is: %s, date is: %s.' % (code, date))
            try:
                TickData.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Error save tick data, code is: %s, date is: %s.' % (code, date))
                logger.error('Error data is: %s' % data)
            else:
                logger.info('Success save tick data, code is: %s, date is: %s.' % (code, date))


def get_tick_data(code, date, retry_count=RETRY_COUNT, pause=PAUSE):
    """获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。"""
    logger.info('Begin get tick data, code is: %s, date is: %s.' % (code, date))
    try:
        data_df = ts.get_tick_data(code, date, retry_count, pause)
    except IOError as e:
        logger.exception('Error get tick data, sleep 5m, then try again. code is: %s.' % code)
        time.sleep(5 * 60)
        get_tick_data(code, date, retry_count, pause)
    except Exception as e:
        logger.exception('Error get tick data, code is :%s, date is %s.' % (code, date))
    else:
        # 当当天没有数据的时候, 返回的都是NaN
        if data_df is not None and not data_df.empty and data_df.price.any():
            data = data_df.values
            tick_data_queue.put((code, date, data))
            logger.info('Success get tick data,  code is :%s, date is %s.' % (code, date))
        else:
            logger.warn('Empty get tick data,  code is :%s, date is %s.' % (code, date))
    # time.sleep(0.5)


def save_today_tick_data():
    """获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。
    
    在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame
      或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，
      当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取.
    """
    logger.info('Begin save today tick data thread.')

    while True:
        if today_tick_data_queue.empty():
            time.sleep(0.01)
        else:
            today_tick_data = today_tick_data_queue.get()
            logger.info('today_tick_data_queue\'s size is: %s' % today_tick_data_queue.qsize())
            code = today_tick_data[0]
            date = today_tick_data[1]
            data = today_tick_data[2]
            # when date is stop, stop this thread. (control in transaction_service)
            if date == 'stop':
                logger.info('Last today tick data stock code is: %s.' % code)
                logger.info('Stop save today tick data thread.')
                break
            logger.info('Get today tick data from tick_data_queue, stock code is: %s, data is: %s'
                        % (code, date))
            data_dicts = [{'code': code, 'date': date, 'time': row[0], 'price': row[1], 'pchange': row[2],
                           'change': row[3], 'volume': row[4], 'amount': row[5], 'type': row[6]}
                          for row in data]
            logger.info('Begin save today tick data, code is: %s, date is: %s.' % (code, date))
            try:
                TickData.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Error save today tick data, code is: %s, date is: %s.' % (code, date))
                logger.error('Error data is: %s' % data)
            else:
                logger.info('Success save today tick data, code is: %s, date is: %s.' % (code, date))


def get_today_tick_data(code, retry_count=RETRY_COUNT, pause=PAUSE):
    """获取个股以往交易历史的分笔数据明细，通过分析分笔数据，可以大致判断资金的进出情况。"""
    logger.info('Begin get today tick data, code is: %s, date is: %s.' % (code, today_line))
    try:
        data_df = ts.get_today_ticks(code, retry_count, pause)
    except Exception as e:
        logger.exception('Error get today tick data, code is :%s, date is %s.' % (code, today_line))
    else:
        if data_df is not None and not data_df.empty:
            data = data_df.values
            today_tick_data_queue.put((code, today_line, data))
            logger.info('Success get today tick data,  code is :%s, date is %s.' % (code, today_line))
        else:
            logger.warn('Empty get today tick data,  code is :%s, date is %s.' % (code, today_line))


########################################################
# big index
########################################################
def save_big_index_data():
    """获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。"""
    logger.info('Begin get and save big index data, date is: %s.' % today_line)
    try:
        data_df = ts.get_index()
    except Exception as e:
        logger.exception('Error get big index data, date is: %s.' % today_line)
    else:
        if data_df is not None and not data_df.empty:
            data = data_df.values
            data_dicts = [{'date': today_line, 'code': row[0], 'name': row[1], 'change': row[2], 'open': row[3],
                           'preclose': row[4], 'close': row[5], 'high': row[6], 'low': row[7],
                           'volume': row[8], 'amount': row[9]} for row in data]
            try:
                BigIndexData.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Error save big index data, date is: %s.' % today_line)
                logger.error('Error data is: %s.' % data)
            else:
                logger.info('Success save big index data, date is: %s.' % today_line)
        else:
            logger.warn('Empty save big index data, date is: %s.' % today_line)


########################################################
# big trade data
########################################################
def save_big_trade_data():
    logger.info('Begin save big trade data thread.')
    while True:
        if big_trade_data_queue.empty():
            time.sleep(0.01)
        else:
            big_trade_data = big_trade_data_queue.get()
            logger.info('big_trade_data_queue\'s size is: %s' % big_trade_data_queue.qsize())
            code = big_trade_data[0]
            date = big_trade_data[1]
            data = big_trade_data[2]
            # when date is stop, stop this thread. (control in transaction_service)
            if date == 'stop':
                logger.info('Last big trade data stock code is: %s.' % code)
                logger.info('Stop save big trade data thread.')
                break
            logger.info('Get big trade data from big_trade_data_queue, stock code is: %s, data is: %s'
                        % (code, date))
            data_dicts = [{'date': date, 'code': row[0], 'name': row[1], 'time': row[2], 'price': row[3],
                           'volume': row[4], 'preprice': row[5], 'type': row[6]} for row in data]
            logger.info('Begin save big trade data, code is: %s, date is: %s.' % (code, date))
            try:
                BigTradeData.insert_many(data_dicts).execute()
            except Exception as e:
                logger.exception('Error save big trade data, code is: %s, date is: %s.' % (code, date))
                logger.error('Error data is: %s' % data)
            else:
                logger.info('Success save big trade data, code is: %s, date is: %s.' % (code, date))


def get_big_trade_data(code, date, vol=400, retry_count=RETRY_COUNT, pause=PAUSE):
    """获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。"""
    logger.info('Begin get big trade data, code is: %s, date is: %s.' % (code, date))
    try:
        data_df = ts.get_sina_dd(code, date, vol, retry_count, pause)
    except Exception as e:
        logger.exception('Error get big trade data, code is: %s, date is: %s.' % (code, date))
    else:
        if data_df is not None and not data_df.empty:
            data = data_df.values
            big_trade_data_queue.put((code, date, data))
            logger.info('Success get big trade data, code is: %s, date is: %s.' % (code, date))
        else:
            logger.warn('Empty get big trade data, code is: %s, date is: %s.' % (code, date))


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
