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
    # bser.save_yesterday_all_stocks_his_data()
    # bser.save_today_all_stocks_his_data()
    # bser.save_all_stocks_his_data(start=util.get_ndays_before_line(6), end=yesterday_line)
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


def save_select_stocks_hist_data(start=None, end=None, ktype=None):
    """保存选择股票的交易数据"""
    
    stock_codes = ['600622']
    logger.info('Begin save select stocks history data')
    bser.save_select_stocks_hist_data(stocks=stock_codes, start_date=start, end_date=end, ktype=ktype)
    logger.info('End save select stocks history data')


def save_select_stocks_h_data_revote(start=None, end=None, autype='qfp', index=False):
    stock_codes = ['600622']
    bser.save_select_stocks_h_data_revote(stock_codes, start_date=start, end_date=end, autype=autype, index=index)



def main():
    parser = argparse.ArgumentParser(description='Get stock data with tushare')

    def args_parse():
        """参数解析"""

        top_sub_parsers = parser.add_subparsers()

        # database table parser
        db_parser = top_sub_parsers.add_parser('d', help='database and table service')
        db_parser.add_argument('-d', action='store_true', dest='drop_table', help='drop all tables')
        db_parser.add_argument('-c', action='store_true', dest='create_table', help='create all tables')

        # transaction parser
        transaction_parser = top_sub_parsers.add_parser('t', help='transaction service')
        tran_sub_parsers = transaction_parser.add_subparsers()
        hist_parser = tran_sub_parsers.add_parser('h', help='hist data service')
        hist_parser.add_argument('-hi', action='store_true',
                                 dest='save_stocks_hist_data',
                                 help='save stocks history data')
        hist_parser.add_argument('-r', action='store_true',
                                 dest='save_stocks_revote_hist_data',
                                 help='save stocks revote history data')
        hist_parser.add_argument('-tick', action='store_true',
                                 dest='save_tick_data',
                                 help='save tick data(获取历史的分笔数据明细)')
        hist_parser.add_argument('-ttick', action='store_true',
                                 dest='save_today_tick_data',
                                 help='save today tick data(获取当前交易日（交易进行中使用))')
        hist_parser.add_argument('-bt', action='store_true',
                                 dest='save_big_trade_data',
                                 help='save big trade data(获取大单交易数据)')
        hist_parser.add_argument('-bi', action='store_true',
                                 dest='save_big_index_data',
                                 help='save big index data(获取大盘指数实时行情列表)')

        transaction_parser.add_argument('-t', action='store_true',
                                        dest='today_data',
                                        help='save today stocks history data')
        transaction_parser.add_argument('-y', action='store_true',
                                        dest='yesterday_data',
                                        help='save yesterday stocks history data')
        transaction_parser.add_argument('--start', dest='start_date', help='start date')
        transaction_parser.add_argument('--end', dest='end_date', help='end date')
        transaction_parser.add_argument('--ktype', dest='ktype',
                                        help='数据类型: D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟',
                                        choices=['D', 'W', 'M', '5', '15', '30', '60'])
        transaction_parser.add_argument('-a', action='store_true', dest='all_stocks', help='get all stocks data.')
        transaction_parser.add_argument('-s', action='store_true', dest='select_stocks', help='get select stocks data.')

        # fundamentals, basic parser
        fundamentals_parser = top_sub_parsers.add_parser('f', help='fundamentals service(include stock list)')
        fundamentals_parser.add_argument('-s', action='store_true', dest='save_stocks_basic_data',
                                         help='save stocks basic data')
        _args = parser.parse_args()
        logger.debug(_args)
        return _args
    args = args_parse()

    # fundamentals
    if hasattr(args, 'save_stocks_basic_data') and args.save_stocks_basic_data:
        base_service.save_stocks_basic_data()

    # transaction
    if hasattr(args, 'save_stocks_hist_data') and args.save_stocks_hist_data:
        if args.all_stocks:
            if args.today_data:
                bser.save_all_stocks_hist_data(today_line, today_line, ktype=args.ktype)
            elif args.yesterday_data:
                bser.save_all_stocks_hist_data(yesterday_line, yesterday_line, ktype=args.ktype)
            else:
                bser.save_all_stocks_hist_data(args.start_date, args.end_date, ktype=args.ktype)
        if args.select_stocks:
            if args.today_data:
                save_select_stocks_hist_data(today_line, today_line, ktype=args.ktype)
            elif args.yesterday_data:
                save_select_stocks_hist_data(yesterday_line, yesterday_line, ktype=args.ktype)
            else:
                save_select_stocks_hist_data(args.start_date, args.end_date, ktype=args.ktype)
        else:
            logger.error('Save stocks hist data must assign -a(all stocks) or -s(select stocks).')
    if hasattr(args, 'save_stocks_revote_hist_data') and args.save_stocks_revote_hist_data:
        if args.all_stocks:
            if args.today_data:
                bser.save_all_stock_h_data_revote(today_line, today_line)
            elif args.yesterday_data:
                bser.save_all_stock_h_data_revote(yesterday_line, yesterday_line)
            else:
                bser.save_all_stock_h_data_revote(args.start_date, args.end_date)
        if args.select_stocks:
            if args.today_data:
                save_select_stocks_h_data_revote(today_line, today_line)
            elif args.yesterday_data:
                save_select_stocks_h_data_revote(yesterday_line, yesterday_line)
            else:
                save_select_stocks_h_data_revote(args.start_date, args.end_date)
        else:
            logger.error('Save stocks revote hist data must assign -a(all stocks) or -s(select stocks).')

    # database and table
    if hasattr(args, 'drop_table') and args.drop_table:
        table_service.drop_all_tables()
    if hasattr(args, 'create_table') and args.create_table:
        table_service.create_all_tables()


    # create_tables()
    # save_data()
    # save_all_days_select_stocks_hist_data()
    # dser.save_his_data_scd('600848',start = '2016-10-13', end = '2016-10-14')
    # stock_classified()
    # table_service.create_tables()
    # bser.save_news()
    

if __name__ == '__main__':
    setup_logging()
    main()
