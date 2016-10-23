import sys
from configparser import ConfigParser
import tushare as ts
from peewee import *
from data import stock_classified as sc
from macro_data import macroscopic_data as md
import logging
import logging.config
from data import base_data as bd
from models import model
from service import data_service as dser
from service import business_service as bser
from utils import util


today = util.get_today()
today_line = util.get_today_line()

yestoday = util.get_yestoday()
yestoday_line = util.get_yestoday_line()
before_yestd_line = util.get_before_yestd_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()
logging.config.fileConfig("logging.conf")
logger = logging.getLogger()

def stock_classified():
    print('begin')
    #sme = sc.SmeClassified()
    # sme.create_sme_classified()
    #sme.save_sme_classified()
    #area = sc.AreaClassified()
    #area.create_area_classified()
    #area.save_area_classified()
    #print('begin gem')
    #gem = sc.GemClassified()
    #gem.create_gem_classified()
    #gem.save_gem_classified()
    #print('begin st')
    #st = sc.StClassified()
    #st.create_st_classified()
    #st.save_st_classified()
    #print('begin hs300')
    #hs300 = sc.Hs300()
    #hs300.create_hs300s()
    #hs300.save_hs300s()
    #print('begin sz50')
    #sz50 = sc.Sz50()
    #sz50.create_sz50s()
    #sz50.save_sz50s()
    #print('begin zz500')

    #zz500 = sc.Zz500()
    #zz500.create_zz500s()
    #zz500.save_zz500s()
    #print('begin terminate')
    #ter = sc.Terminated()
    #ter.create_terminated()
    #ter.save_terminated()
    print('begin suspend')
    suspend = sc.Suspend()
    #suspend.create_suspend()
    suspend.save_suspend()

    
    print('end')

def macro_data():
    '''宏观数据'''
    print('begin macroscopic data')
    #print('egin deposit rate')
    #dep_rate = md.DepositRate()
    #dep_rate.create_dr_table()
    #dep_rate.save_dr_data()

    #print('begin loan rate')
    #loan_rate = md.LoanRate()
    #loan_rate.create_lr_table()
    #loan_rate.save_lr_data()
    #print('end')
    rrr = md.ReserveRequirementRatio()
    rrr.create_table()
    rrr.save_data(date='2010-11-29')

    
def base_data():
    '''基本面数据'''
    print('begin base data')
    #stock_basic = bd.StockBasic() 
    bd.StockBasic.create_tbl()
    #print('created table')
    bd.StockBasic.save_data()
    print('end')


def save_data():
    """下载并保持交易数据"""
    
    # logger.info('Begin save all stocks history data')
    # bser.save_all_stocks_his_data()
    # logger.info('End save all stocks history data')
    # print('End save all stocks history data')

    print('Begin save today all stocks history data')
    logger.info('Begin save today all stocks history data')
    # bser.save_today_all_stocks_his_data()
    bser.save_all_stocks_his_data(start=before_yestd_line, end=yestoday_line)
    logger.info('End save today all stocks history data')
    print('End save today all stocks history data')
 
    # logger.info('Begin save today all data')
    # bser.save_today_all_data()
    # logger.info('End save today all data')
    # print('End save today all data')

    # logger.info('Begin save tick data')
    # bser.save_tick_data()
    # logger.info('End save tick data')
    # print('End save tick data')

def main():
    #macro_data()
    #base_data()
    #model.create_tables()
    #dser.get_stocks()
    # dser.save_his_data_scd('600848',start = '2016-10-13', end = '2016-10-14')
    save_data()


if __name__ == '__main__':
    main()
    
