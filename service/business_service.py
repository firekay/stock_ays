import service.data_service as dsvc
import logging
import logging.config
from utils import util
import threading
import time
from models.model import *


today = util.get_today()
today_line = util.get_today_line()

yestoday = util.get_yestoday()
yestoday_line = util.get_yestoday_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()

def save_all_stocks_his_data(start=None, end=None):
    """下载并保持所有的股票的数据：D, W, M, 5, 15, 30, 60"""
    
    
    threading.Thread(name='save_his_data', target=dsvc.save_his_data).start()
    threading.Thread(name='save_his_data_scd', target=dsvc.save_his_data_scd).start()
    stocks = dsvc.get_stocks()
    i = 0
    for stock in stocks:
        i = i + 1
        #if i == 160:
            #time.sleep(10)
            #i = 0
        threading.Thread(name='get_his_data_' + str(i), target=dsvc.get_his_data, args=(stock.code, start, end)).start()
        threading.Thread(name='get_his_data_scd_' + str(i), target=dsvc.get_his_data_scd, args=(stock.code, start, end)).start()
        time.sleep(0.5)
        #dsvc.save_his_data(stock.code,start=start, end=end, ktype='D')
        #dsvc.save_his_data(stock.code,start=start, end=end)
        #dsvc.save_his_data_scd(stock.code,start=start, end=end)
        
        
def save_today_all_stocks_his_data():
    """下载并保存当天数据"""
    save_all_stocks_his_data(today_line, tomorrow_line)

    
    
    
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
    print('End save tick data: ' + date)


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
    print('End save big trade data: ' + date)


def save_one_years_big_trade_data():
    """获取近一年大盘指数实时行情列表。"""
    for date in [ date for date in (datetime.datetime.now() + datetime.timedelta(-n) for n in range(365))]:
        __save_big_trade_data(date.strftime('%Y-%m-%d'))


def save_today_big_trade_data():
    """获取当天大盘指数实时行情列表。"""
    __save_big_trade_data(today_line)


def save_industry_classified():
    """处理行业分类"""
    print('save_industry_classified')
    dsvc.truncate_table(IndustryClassified)
    dsvc.save_industry_classified()


def save_concept_classified():
    """处理股票概念分类.现实的二级市场交易中，经常会以”概念”来炒作，在数据分析过程中，可根据概念分类监测资金等信息的变动情况。"""
    dsvc.truncate_table(ConceptClassified)
    dsvc.save_concept_classified()


def save_area_classified():
    """按地域对股票进行分类，即查找出哪些股票属于哪个省份。"""
    dsvc.truncate_table(AreaClassified)
    dsvc.save_area_classified()

    
def save_sme_classified():
    """获取中小板股票数据，即查找所有002开头的股票"""
    dsvc.truncate_table(SmeClassified)
    dsvc.save_sme_classified()


def save_gem_classified():
    """获取创业板股票数据，即查找所有300开头的股票"""
    dsvc.truncate_table(GemClassified)
    dsvc.save_gem_classified()


def save_st_classified():
    """获取风险警示板股票数据，即查找所有st股票"""
    dsvc.truncate_table(StClassified)
    dsvc.save_st_classified()


def save_hs300s():
    """获取沪深300当前成份股及所占权重"""
    dsvc.truncate_table(Hs300)
    dsvc.save_hs300s()


def save_sz50s():
    """上证50成分股"""
    dsvc.truncate_table(Sz50)
    dsvc.save_sz50s()


def save_zz500s():
    """中证500成分股"""
    dsvc.truncate_table(Zz500)
    dsvc.save_zz500s()


def save_terminated():
    """获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    dsvc.truncate_table(Terminated)
    dsvc.save_terminated()


def save_suspend():
    """获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    dsvc.truncate_table(Suspend)
    dsvc.save_suspend()


























