# encoding: UTF-8
import os
import yaml
import sys
from configparser import ConfigParser
import tushare as ts
from peewee import *
from data import stock_classified as sc
import logging
from data import base_data as bd
from models import model
from service import data_service as dser
from service import table_service
from service import business_service as bser
from service import base_service
from strategys import common_strategy as cstg
from utils import util
from strategys import common_strategy as cmstg

logger = logging.getLogger(__name__)
today = util.get_today()
today_line = util.get_today_line()

yestoday = util.get_yestoday()
yestoday_line = util.get_yestoday_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()

reload(sys)
sys.setdefaultencoding('utf8')


def setup_logging(
        default_path='resources/logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def stock_classified():
    print('stock classified begin')
    bser.save_industry_classified()
    bser.save_concept_classified()
    bser.save_area_classified()
    bser.save_sme_classified()
    bser.save_gem_classified()
    bser.save_st_classified()
    bser.save_hs300s()
    bser.save_sz50s()
    bser.save_zz500s()
    bser.save_terminated()
    bser.save_suspend()
    print('stock classified end')
    
    sme = sc.SmeClassified()
    sme.create_sme_classified()
    sme.save_sme_classified()
    area = sc.AreaClassified()
    area.create_area_classified()
    area.save_area_classified()
    print('begin gem')
    gem = sc.GemClassified()
    gem.create_gem_classified()
    gem.save_gem_classified()
    print('begin st')
    st = sc.StClassified()
    st.create_st_classified()
    st.save_st_classified()
    print('begin hs300')
    hs300 = sc.Hs300()
    hs300.create_hs300s()
    hs300.save_hs300s()
    print('begin sz50')
    sz50 = sc.Sz50()
    sz50.create_sz50s()
    sz50.save_sz50s()
    print('begin zz500')

    zz500 = sc.Zz500()
    zz500.create_zz500s()
    zz500.save_zz500s()
    print('begin terminate')
    ter = sc.Terminated()
    ter.create_terminated()
    ter.save_terminated()
    print('begin suspend')
    suspend = sc.Suspend()
    suspend.create_suspend()
    suspend.save_suspend()
    
    print('end')


# def macro_data():
#     """宏观数据"""
#     print('begin macroscopic data')
#     print('egin deposit rate')
#     dep_rate = md.DepositRate()
#     dep_rate.create_dr_table()
#     dep_rate.save_dr_data()
#
#     print('begin loan rate')
#     loan_rate = md.LoanRate()
#     loan_rate.create_lr_table()
#     loan_rate.save_lr_data()
#     print('end')
#     rrr = md.ReserveRequirementRatio()
#     rrr.create_table()
#     rrr.save_data(date='2010-11-29')


def drop_tables():
    logger.info('Begin drop tables.')
    table_service.drop_all_tables()
    logger.info('End drop tables.')


def create_tables():
    logger.info("Create tables begin.")
    table_service.create_all_tables()
    logger.info("Create tables end.")


def save_select_stock_code_data():
    stock_codes = ['600623', '600622', '603999', '600619', '600629', '600617', '600602', '600620', '600618', '600621']
    logger.info('Begin save select stocks history data')
    bser.save_select_stocks_his_data(stocks=stock_codes, ktype='W')
    logger.info('End save select stocks history data')


def save_data():
    """下载并保持交易数据"""
    
    logger.info('Begin save all stocks history data')
    bser.save_all_stocks_his_data()
    logger.info('End save all stocks history data')

    # logger.info('Begin save today all stocks history data')
    # bser.save_yestoday_all_stocks_his_data()
    # bser.save_today_all_stocks_his_data()
    # bser.save_all_stocks_his_data(start=util.get_ndays_before_line(6), end=yestoday_line)
    # logger.info('End save today all stocks history data')
    #
    # logger.info('Begin save today all data')
    # bser.save_today_all_data()
    # logger.info('End save today all data')
    # print('End save today all data')
    #
    # logger.info('Begin save tick data')
    # bser.save_tick_data()
    # logger.info('End save tick data')
    # print('End save tick data')


def strategy():
    cstg.macd_service()


def main():
    # drop_tables()
    # create_tables()
    # base_service.save_stocks_basic_data()
    # save_data()
    save_select_stock_code_data()
    # dser.save_his_data_scd('600848',start = '2016-10-13', end = '2016-10-14')
    # stock_classified()
    # table_service.create_tables()
    # bser.save_news()
    

if __name__ == '__main__':
    setup_logging()
    main()
