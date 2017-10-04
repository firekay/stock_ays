# encoding: UTF-8
import logging
import threading
from models.model import *
from dal import classification_dal
from dal import util_dal
from dal import transaction_dal
from service import base_service
from service import table_service
import pandas as pd
import tushare as ts
from utils import util

logger = logging.getLogger(__name__)
today = util.get_today()
today_line = util.get_today_line()

yesterday = util.get_yesterday()
yesterday_line = util.get_yesterday_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()

RETRY_COUNT = 5


def check_thread_alive(thread):
    logger.info('Thread %s is also alive.' % thread.getName())
    if not thread.is_alive:
        logger.warn('Thread %s not alive.' % thread.getName())


def save_stocks_k_data(stocks=None, start_date='', end_date='', autype='qfq', index=False,
                       ktype=None):
    """获取k线数据的历史复权数据
    
    新接口融合了get_hist_data和get_h_data两个接口的功能，即能方便获取日周月的低频数据，
    也可以获取5、15、30和60分钟相对高频的数据。
    同时，上市以来的前后复权数据也能在一行代码中轻松获得，当然，您也可以选择不复权。
    
    Args:
        stocks:list,股票代码 e.g. ['600848', '000001'], 为None, 则取stock_basic中所有的股票
        start_date:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
        end_date:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
        autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
        index:Boolean，是否是大盘指数，默认为False
        ktype: 数据类型: D, W M, 默认为D
    """
    ktypes = ['D', 'W', 'M']
    log_save_type = 'all'
    assert ktype in ktypes, 'ktype must be one of %s' % ktypes
    if ktype.upper() == 'D':
        model = HistoryDataD
    elif ktype.upper() == 'W':
        model = HistoryDataW
    elif ktype.upper() == 'M':
        model = HistoryDataM

    if stocks:
        assert isinstance(stocks, list), 'stocks must be a list type.'
        log_save_type = 'select'
    else:
        stocks = [stock.code for stock in base_service.get_stocks()]
    last_stock_code = stocks[-1]
    logger.info('Last stock code is: %s' % last_stock_code)
    save_stock_k_data_thread = threading.Thread(name='save_stock_k_data', target=transaction_dal.save_stock_k_data,
                                                args=(last_stock_code,))
    save_stock_k_data_thread.start()
    # threading.Timer(1, check_thread_alive, args=(save_stock_k_data_thread,)).start()
    if end_date != '':
        assert start_date != '', 'start_date must be not None, when end_date != ''.'
    if start_date != '':
        if end_date == '':
            end_date = today_line
        logger.info('Begin save %s stocks history k data, start date is: %s, end date is: %s, ktype is: %s.' %
                    (log_save_type, start_date, end_date, ktype))
    else:
        logger.info('Begin save %s stocks history k data, all date, ktype is: %s.' % (log_save_type, ktype))
    for stock in stocks:
        if ktype:
            if start_date == '':
                deleted = util_dal.delete_code_data(model, stock)
            else:
                deleted = util_dal.delete_code_start_date_end_date_data(model, stock,
                                                                        start_date, end_date)
            if deleted:
                transaction_dal.get_stock_k_data(stock, start_date, end_date, autype, index, ktype)
        else:
            for ktype in ktypes:
                if start_date == '':
                    deleted = util_dal.delete_code_data(model, stock)
                else:
                    deleted = util_dal.delete_code_start_date_end_date_data(model, stock,
                                                                            start_date, end_date)
                if deleted:
                    transaction_dal.get_stock_k_data(stock, start_date, end_date, autype, index, ktype)
    if start_date != '':
        logger.info('End save %s stocks history k data, start date is: %s, end date is: %s, ktype is: %s.' %
                    (log_save_type, start_date, end_date, ktype))
    else:
        logger.info('End save %s stocks history k data, all date, ktype is: %s.' % (log_save_type, ktype))


def save_stocks_hist_data(stocks=None, start_date=None, end_date=None, ktype=None):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线数据。
    本接口只能获取近3年的日线数据
    """
    log_save_type = 'all'
    ktypes = list(['D', 'W', 'M'])
    assert ktype in ktypes, 'ktype must be one of %s' % ktypes
    if ktype.upper() == 'D':
        model = HistoryDataD
    elif ktype.upper() == 'W':
        model = HistoryDataW
    elif ktype.upper() == 'M':
        model = HistoryDataM
    # elif ktype == '5':
    #     model = HistoryData5

    if stocks:
        assert isinstance(stocks, list), 'stocks must be list.'
        log_save_type = 'select'
    else:
        stocks = [stock.code for stock in base_service.get_stocks()]
    last_stock_code = stocks[-1]
    logger.info('last_stock_code is: %s' % last_stock_code)
    save_his_data_thread = threading.Thread(name='save_his_data',
                                            target=transaction_dal.save_his_data, args=(last_stock_code,))
    save_his_data_thread.start()
    if end_date is not None:
        assert start_date is not None, 'start_date must be not None, when end_date is not None.'
    if start_date is not None:
        if end_date is None:
            end_date = today_line
        logger.info('Begin save %s stocks history data, start date is: %s, end date is: %s, ktype is: %s.'
                    % (log_save_type, start_date, end_date, ktype))
    else:
        logger.info('Begin save %s stocks history data, all date, ktype is: %s.'
                    % (log_save_type, ktype))

    for stock in stocks:
        if ktype is None:
            for ktype in ktypes:
                if start_date is None:
                    deleted = util_dal.delete_code_data(model, stock)
                else:
                    deleted = util_dal.delete_code_start_date_end_date_data(model, stock,
                                                                            start_date, end_date)
                if deleted:
                    transaction_dal.get_his_data(stock, start_date=start_date, end_date=end_date, ktype=ktype)
        else:
            if start_date is None:
                deleted = util_dal.delete_code_data(model, stock)
            else:
                deleted = util_dal.delete_code_start_date_end_date_data(model, stock,
                                                                              start_date, end_date)
            if deleted:
                transaction_dal.get_his_data(stock, start_date=start_date, end_date=end_date, ktype=ktype)

    if start_date is not None:
        logger.info('End save %s stocks history data, start date is: %s, end date is: %s, ktype is: %s.'
                    % (log_save_type, start_date, end_date, ktype))
    else:
        logger.info('End save %s stocks history data, all date, ktype is: %s.'
                    % (log_save_type, ktype))


def save_stock_h_data_revote(stocks=None, start_date=None, end_date=None, autype='qfp', index=False):
    """获取B{所有}历史复权数据
    
    Args:
        stocks:list,股票代码 e.g. ['600848', '000001'], 为None, 则取stock_basic中所有的股票
        start_date:string,开始日期 format：YYYY-MM-DD 为空时取当前日期
        end_date:string,结束日期 format：YYYY-MM-DD 为空时取去年今日
        autype:string,复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
        index:Boolean，是否是大盘指数，默认为False
        retry_count : int, 默认3,如遇网络等问题重复执行的次数
        pause : int, 默认 0,重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    """
    ktypes = ['D', 'W', 'M']
    log_save_type = 'all'

    if stocks:
        assert isinstance(stocks, list), 'stocks must be a list type.'
        log_save_type = 'select'
    else:
        stocks = [stock.code for stock in base_service.get_stocks()]
    last_stock_code = stocks[-1]
    logger.info('Last stock code is: %s' % last_stock_code)
    save_h_revote_data_thread = threading.Thread(name='save_h_revote_data',
                                                 target=transaction_dal.save_h_revote_data, args=(last_stock_code,))
    save_h_revote_data_thread.start()
    # threading.Timer(1, check_thread_alive, args=(save_h_revote_data_thread,)).start()
    if end_date is not None:
        assert start_date is not None, 'start_date must be not None, when end_date is not None.'
    if start_date is not None:
        if end_date is None:
            end_date = today_line
        logger.info('Begin save %s stocks history h revote data, start date is: %s, end date is: %s.' %
                    (log_save_type, start_date, end_date))
    else:
        logger.info('Begin save %s stocks history k data, all date.' % log_save_type)
    for stock in stocks:
        if start_date is None:
            deleted = util_dal.delete_code_data(RevoteHistoryData, stock)
        else:
            deleted = util_dal.delete_code_start_date_end_date_data(RevoteHistoryData, stock, start_date, end_date)
        if deleted:
            transaction_dal.get_h_revote_data(stock, start_date, end_date, autype, index)
    if start_date is not None:
        logger.info('End save %s stocks history h revote data, start date is: %s, end date is: %s.' %
                    (log_save_type, start_date, end_date))
    else:
        logger.info('End save %s stocks history k data, all date.' % log_save_type)


def save_yesterday_all_stocks_hist_data(ktype=None):
    """下载并保存昨天数据"""
    save_stocks_hist_data(yesterday_line, yesterday_line, ktype=ktype)


def save_today_all_stocks_hist_data(ktype=None):
    """下载并保存当天数据"""
    save_stocks_hist_data(today_line, today_line, ktype=ktype)

#
# def save_realtime_quetes2file(codes):
#     def _deal_realtime_quotes_data(codes):
#         data_df = transaction_dal.get_realtime_quotes(codes)


def save_today_all_data():
    """一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）"""
    transaction_dal.save_today_all_data()


def save_tick_data(stocks, date):
    """获取给定日期的交易历史的分笔数据明细.

    通过分析分笔数据，可以大致判断资金的进出情况。在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取.
    当code为None,或者code长度不为6,或者date为None时直接返回None"""

    last_stock_code = None
    log_save_type = 'all'

    if stocks is None:
        stocks = base_service.get_stocks()
    else:
        assert isinstance(stocks, list), 'stocks must be a list type.'
        last_stock_code = stocks[-1]
        log_save_type = 'select'
    logger.info('Last stock code is: ' + last_stock_code)
    logger.info('Begin save %s tick data, date is: %s' % (log_save_type, date))
    for stock in stocks:
        transaction_dal.save_tick_data(stock.code, date)
    save_tick_data_thread = threading.Thread(name='save_tick_data', target=transaction_dal.save_tick_data,
                                             args=(last_stock_code,))
    save_tick_data_thread.start()
    threading.Timer(1, check_thread_alive, args=(save_tick_data_thread,)).start()
    for stock in stocks:
        transaction_dal.get_tick_data(stock, date)
    logger.info('End save %s tick data, date is: %s' % (log_save_type, date))


def save_tick_data(stocks, start_date, end_date):
    """获取给定日期范围的交易历史的分笔数据明细."""
    for date_mid in util.range_date(start_date, end_date):
        save_tick_data(stocks, date_mid)


# TODO: Add get_today_ticks method
# def save_tick_data_today():
#     """获取今日交易的历史分笔数据"""
#     save_tick_data(today_line)
#
#
# def save_one_years_tick_data():
#     """获取近一年交易的历史分笔数据"""
#     for date in [ date for date in (datetime.datetime.now() + datetime.timedelta(-n) for n in range(365))]:
#         save_tick_data(date.strftime('%Y-%m-%d'))


def save_big_index_data():
    """获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。"""
    transaction_dal.save_big_index_data()


def save_big_trade_data(stocks=None, start_date=None, end_date=None):
    """获取大单交易数据，默认为大于等于400手，数据来源于新浪财经。
    
    Args:
        stocks: 股票列表, 为空则代表全部
        start_date: 开始时间, 为空代表当天
        end_date: 结束时间. 为空则表示只有start_date启动用, 
                        并且如果开始时间为空则end_date无意义,
                        否则, 得到的是start_date与end_date之间的数据.
        """
    last_stock_code = None
    log_save_type = 'all'

    if not stocks:
        stocks = base_service.get_stocks()
    else:
        assert isinstance(stocks, list), 'stocks must be a list type.'
        last_stock_code = stocks[-1]
        log_save_type = 'select'
    logger.info('Last stock code is: ' + last_stock_code)
    if start_date:
        # 没有end_date的时候, 得到的是start_date这一天的, 否则调用start到end(不包括)之间的数据
        if end_date:
            logger.info('Begin save %s big trade data, start date is: %s, end date is: %s.' %
                        (log_save_type, start_date, end_date))
            [transaction_dal.save_big_trade_data(stock, date_mid)
             for date_mid in util.range_date(start_date, end_date)
             for stock in stocks]
        else:
            logger.info('Begin save %s big trade data, the date is: %s.' %
                        (log_save_type, start_date))
            [transaction_dal.save_big_trade_data(stock.code, start_date) for stock in stocks]
    # 没有start_date, 则调用的是当天的数据
    else:
        start_date = util.get_today_line()
        logger.info('Begin save %s big trade data, the date is: %s.' %
                    (log_save_type, start_date))
        [transaction_dal.save_big_trade_data(stock.code, start_date) for stock in stocks]
    # for logs
    if start_date:
        if end_date:
            logger.info('End save %s big trade data, start date is: %s, end date is: %s.' %
                        (log_save_type, start_date, end_date))
    else:
        logger.info('End save %s big trade data, the date is: %s.' %
                    (log_save_type, start_date))


# def save_news():
#     """获取即时财经新闻，类型包括国内财经、证券、外汇、期货、港股和美股等新闻信息。数据更新较快，使用过程中可用定时任务来获取。
#
#     根据time和url的元组来判断数据库中是否有数据， 如果存在此新闻就不加入， 如果不存在就插入到mongodb中。
#     """
#     # news_df = transaction_dal.get_news(top=5)
#     # transaction_dal.save_news2mongo(news_df)
#     # 数据写入csv文件
#     # news_df.to_csv('logs/latest_news.csv', sep='\t', encoding='utf-8')
#
#     # 从数据库中初始化time_urls， 不再添加已有的新闻
#     # TODO: 改为通过url来定义唯一新闻
#     time_urls = set(transaction_dal.get_news_time_and_url_in_mongo())
#     while(True):
#         logger.info('The size of time_urls is: %d' % len(time_urls))
#         news_df = transaction_dal.get_news(top=5)
#         if(news_df is not None):
#             news_time_urls = [tuple(time_url) for time_url in news_df[['time', 'url']].values]
#             # return type str not a type tuple
#             # news_time_urls = news_df[['time', 'url']].apply(lambda x: "('{}', '{}')".format(x[0], x[1]), axis=1)
#             for i, time_url in enumerate(news_time_urls):
#                 if(time_url not in time_urls):
#                     time_urls.add(time_url)
#                 else:
#                     news_df.drop(i, inplace=True)
#
#             # TODO: drop不能删掉元素， 重新写
#             #for i, time in enumerate(news_times):
#                 #if(time in times):
#                     #news_df.drop(i)
#                 #else:
#                     #times.add(time)
#             if(not news_df.empty):
#                 transaction_dal.save_news2mongo(news_df)
#         time.sleep(60)
