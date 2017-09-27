# encoding: UTF-8
import os
import yaml
import sys
import argparse
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

yesterday = util.get_yesterday()
yesterday_line = util.get_yesterday_line()

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


def save_all_transaction_data():
    """下载并保存所有交易数据"""
    
    # logger.info('Begin save all stocks history data')
    # bser.save_all_days_all_stocks_hist_data()
    # logger.info('End save all stocks history data')

    # logger.info('Begin save today all stocks history data')
    bser.save_yestoday_all_stocks_his_data()
    # bser.save_today_all_stocks_his_data()
    # bser.save_all_stocks_his_data(start=util.get_ndays_before_line(6), end=yestoday_line)
    # logger.info('End save today all stocks history data')
    #
    # logger.info('Begin save today all data')
    bser.save_today_all_data()
    # logger.info('End save today all data')
    # print('End save today all data')
    #
    # logger.info('Begin save tick data')
    # bser.save_tick_data()
    # logger.info('End save tick data')
    # print('End save tick data')


def strategy():
    cstg.macd_service()


def save_select_stocks_hist_data(start=None, end=None):
    stock_codes = ['600622']
    logger.info('Begin save select stocks history data')
    bser.save_all_days_select_stocks_hist_data(stocks=stock_codes, start=start, end=end, ktype='W')
    logger.info('End save select stocks history data')


def main():
    parser = argparse.ArgumentParser(description='Get stock data with tushare')

    def args_parse():
        """参数解析"""

        table = parser.add_argument_group('table service')
        table.add_argument('-d', action='store_true', dest='drop_table', help='drop all tables')
        table.add_argument('-c', action='store_true', dest='create_table', help='create all tables')

        transaction = parser.add_argument_group('transaction')

        transaction.add_argument('-t-a-a-h-d', action='store_true', dest='save_all_days_all_stocks_hist_data', help='save all days all stocks history data')
        transaction.add_argument('-t-a-s-h-d', action='store_true', dest='save_all_days_select_stocks_hist_data', help='save all days selected all stocks history data')

        transaction.add_argument('-t-t-a-h-d', action='store_true', dest='save_today_all_stocks_hist_data', help='save today all stocks history data')
        transaction.add_argument('-t-t-s-h-d', action='store_true', dest='save_today_select_stocks_hist_data', help='save today selected stocks history data')

        transaction.add_argument('-t-y-a-h-d', action='store_true', dest='save_yestoday_all_stocks_hist_data', help='save yestoday all stocks history data')
        transaction.add_argument('-t-y-s-h-d', action='store_true', dest='save_yestoday_select_stocks_hist_data', help='save yestoday selected stocks history data')

        # subparsers = parser.add_subparsers()
        # transaction_selected = subparsers.add_parser('-t-a-s-h-d', help='save all selected stocks history data')
        # transaction_selected.add_argument('--stocks', nargs='+', dest='stocks_selected', help='save all selected stocks history data')
        # transaction_selected.add_argument('-ktype', choices=['D', 'W', 'M'], help='save the sotck type, D is day, W is week, M is month')

        _args = parser.parse_args()
        logger.debug(_args)
        return _args
    args = args_parse()
    if args.save_all_days_all_stocks_hist_data:
        bser.save_all_days_all_stocks_hist_data()
    if args.save_all_days_select_stocks_hist_data:
        save_select_stocks_hist_data()
    if args.save_today_all_stocks_hist_data:
        bser.save_today_all_stocks_hist_data()
    if args.save_today_select_stocks_hist_data:
        save_select_stocks_hist_data(today_line, tomorrow_line)
    if args.save_yestoday_all_stocks_hist_data:
        bser.save_yestoday_all_stocks_hist_data()
    if args.save_yestoday_select_stocks_hist_data:
        save_select_stocks_hist_data(yestoday_line, today_line)
    if args.drop_table:
        table_service.drop_all_tables()
    if args.create_table:
        table_service.create_all_tables()

    # create_tables()
    # base_service.save_stocks_basic_data()
    # save_data()
    # save_all_days_select_stocks_hist_data()
    # dser.save_his_data_scd('600848',start = '2016-10-13', end = '2016-10-14')
    # stock_classified()
    # table_service.create_tables()
    # bser.save_news()
    

if __name__ == '__main__':
    setup_logging()
    main()
