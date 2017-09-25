# encoding: UTF-8
import logging
import threading
import threadpool
import time
from models.model import *
import service.data_service as dsvc
from service import table_service
from utils import util


today = util.get_today()
today_line = util.get_today_line()

yestoday = util.get_yestoday()
yestoday_line = util.get_yestoday_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()

logger = logging.getLogger(__name__)


def check_thread_alive(thread):
    logger.info('Thread %s is also alive.' % thread.getName())
    if not thread.is_alive:
        logger.warn('Thread %s not alive.' % thread.getName())


def save_select_stocks_his_data(stocks, start=None, end=None, ktype=None, retry_count=10, pause=0.00):
    """获取个股历史交易数据（包括均线数据），可以通过参数设置获取日k线、周k线、月k线数据。
    本接口只能获取近3年的日线数据
    """
    ktypes = list(['D', 'W', 'M'])
    last_stock_code = stocks[-1]
    logger.info(last_stock_code)
    save_his_data_thread = threading.Thread(name='save_his_data', target=dsvc.save_his_data, args=(last_stock_code,))
    save_his_data_thread.start()

    def _deal_data(code, start, end, ktype, retry_count, pause):
        logger.info('Begin get data: %s,%s,%s' % (code, start, ktype))
        try:
            data_df = ts.get_hist_data(code, start, end, ktype, retry_count, pause)
            if data_df is not None and not data_df.empty:
                data_df['date'] = pd.Series(data_df.axes[0], index=data_df.index)
                data = data_df.values
                dsvc.his_data_queue.put((code, ktype, data))
                logger.info('End get data: %s,%s,%s' % (code, start, ktype))
            else:
                logger.info('Empty get data: %s,%s,%s,%s' % (code, start, end, ktype))
        except Exception as e:
            logger.exception('Get data error: %s,%s,%s' % (code, start, ktype))

    for stock in stocks:
        if ktype is None:
            for ktype in ktypes:
                _deal_data(stock, start, end, ktype, retry_count, pause)
        else:
            _deal_data(stock, start, end, ktype, retry_count, pause)


def save_all_stocks_his_data(start=None, end=None):
    """下载并保持所有的股票的数据：D, W, M, 5, 15, 30, 60"""

    # pool = threadpool.ThreadPool(128)
    # requests = threadpool.makeRequests(dsvc.save_his_data)
    # [pool.putRequest(req) for req in requests]
    # pool.wait()
    save_his_data_thread = threading.Thread(name='save_his_data', target=dsvc.save_his_data)
    save_his_data_thread.start()
    threading.Timer(1, check_thread_alive, args=(save_his_data_thread)).start()

    # threading.Thread(name='save_his_data_scd', target=dsvc.save_his_data_scd).start()

    stocks = dsvc.get_stocks()
    for stock in stocks:
        dsvc.get_his_data(stock.code, start, end)


def save_yestoday_all_stocks_his_data():
    """下载并保存昨天数据"""
    save_all_stocks_his_data(yestoday_line, today_line)


def save_today_all_stocks_his_data():
    """下载并保存当天数据"""
    save_all_stocks_his_data(today_line, tomorrow_line)

    
def save_realtime_quetes2file(codes):
    def _deal_realtime_quotes_data(codes):
        data_df = dsvc.get_realtime_quotes(codes)


def save_today_all_data():
    """一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）"""
    dsvc.save_today_all_data()


def __save_tick_data(date):
    """获取给定日期的交易历史的分笔数据明细.

    通过分析分笔数据，可以大致判断资金的进出情况。在使用过程中，对于获取股票某一阶段的历史分笔数据，需要通过参入交易日参数并append到一个DataFrame或者直接append到本地同一个文件里。历史分笔接口只能获取当前交易日之前的数据，当日分笔历史数据请调用get_today_ticks()接口或者在当日18点后通过本接口获取.
    当code为None,或者code长度不为6,或者date为None时直接返回None"""

    logger.info('Begin save tick data: ' + date)
    stocks = dsvc.get_stocks()
    for stock in stocks:
        dsvc.save_tick_data(stock.code, date)
    logger.info('End save tick data: ' + date)


def save_tick_data_today():
    """获取今日交易的历史分笔数据"""
    __save_tick_data(today_line)


def save_one_years_tick_data():
    """获取近一年交易的历史分笔数据"""
    for date in [ date for date in (datetime.datetime.now() + datetime.timedelta(-n) for n in range(365))]:
        __save_tick_data(date.strftime('%Y-%m-%d'))


def save_big_index_data():
    """获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。"""
    dsvc.save_big_index_data()


def __save_big_trade_data(date):
    """获取大盘指数实时行情列表，以表格的形式展示大盘指数实时行情。"""
    logger.info('Begin save big trade data: ' + date)
    stocks = dsvc.get_stocks()
    for stock in stocks:
        dsvc.save_big_trade_data(stock.code, date)
    logger.info('End save big trade data: ' + date)


def save_one_years_big_trade_data():
    """获取近一年大盘指数实时行情列表。"""
    for date in [ date for date in (datetime.datetime.now() + datetime.timedelta(-n) for n in range(365))]:
        __save_big_trade_data(date.strftime('%Y-%m-%d'))


def save_today_big_trade_data():
    """获取当天大盘指数实时行情列表。"""
    __save_big_trade_data(today_line)


def save_industry_classified():
    """处理行业分类"""
    logger.info('save_industry_classified')
    table_service.truncate_table(IndustryClassified)
    dsvc.save_industry_classified()


def save_concept_classified():
    """处理股票概念分类.现实的二级市场交易中，经常会以”概念”来炒作，在数据分析过程中，可根据概念分类监测资金等信息的变动情况。"""
    table_service.truncate_table(ConceptClassified)
    dsvc.save_concept_classified()


def save_area_classified():
    """按地域对股票进行分类，即查找出哪些股票属于哪个省份。"""
    table_service.truncate_table(AreaClassified)
    dsvc.save_area_classified()

    
def save_sme_classified():
    """获取中小板股票数据，即查找所有002开头的股票"""
    table_service.truncate_table(SmeClassified)
    dsvc.save_sme_classified()


def save_gem_classified():
    """获取创业板股票数据，即查找所有300开头的股票"""
    table_service.truncate_table(GemClassified)
    dsvc.save_gem_classified()


def save_st_classified():
    """获取风险警示板股票数据，即查找所有st股票"""
    table_service.truncate_table(StClassified)
    dsvc.save_st_classified()


def save_hs300s():
    """获取沪深300当前成份股及所占权重"""
    table_service.truncate_table(Hs300)
    dsvc.save_hs300s()


def save_sz50s():
    """上证50成分股"""
    table_service.truncate_table(Sz50)
    dsvc.save_sz50s()


def save_zz500s():
    """中证500成分股"""
    table_service.truncate_table(Zz500)
    dsvc.save_zz500s()


def save_terminated():
    """获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    table_service.truncate_table(Terminated)
    dsvc.save_terminated()


def save_suspend():
    """获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    table_service.truncate_table(Suspend)
    dsvc.save_suspend()


def save_stock_basic():
    table_service.truncate_table(StockBasic)
    dsvc.save_stock_basic()


def save_news():
    """获取即时财经新闻，类型包括国内财经、证券、外汇、期货、港股和美股等新闻信息。数据更新较快，使用过程中可用定时任务来获取。
    
    根据time和url的元组来判断数据库中是否有数据， 如果存在此新闻就不加入， 如果不存在就插入到mongodb中。
    """
    #news_df = dsvc.get_news(top=5)
    #dsvc.save_news2mongo(news_df)
    # 数据写入csv文件
    #news_df.to_csv('logs/latest_news.csv', sep='\t', encoding='utf-8')
    
    # 从数据库中初始化time_urls， 不再添加已有的新闻
    # TODO: 改为通过url来定义唯一新闻
    time_urls = set(dsvc.get_news_time_and_url_in_mongo())
    while(True):
        logger.info('The size of time_urls is: %d' % len(time_urls))
        news_df = dsvc.get_news(top=5)
        if(news_df is not None):
            news_time_urls = [tuple(time_url) for time_url in news_df[['time', 'url']].values]
            #news_time_urls = news_df[['time', 'url']].apply(lambda x: "('{}', '{}')".format(x[0], x[1]), axis=1) # return type str not a type tuple
            for i, time_url in enumerate(news_time_urls):
                if(time_url not in time_urls):
                    time_urls.add(time_url)
                else:
                    news_df.drop(i, inplace=True)
                    
            # TODO: drop不能删掉元素， 重新写
            #for i, time in enumerate(news_times):
                #if(time in times):
                    #news_df.drop(i)
                #else:
                    #times.add(time)
            if(not news_df.empty):
                dsvc.save_news2mongo(news_df)
        time.sleep(60)
        
                
