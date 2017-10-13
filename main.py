# encoding: UTF-8
import argparse
import logging
import os
import sys
import yaml
from data import stock_classified as sc
from service import bank_loan_call_rate_service as blservice
from service import base_service
from service import classfication_service
from service import investment_ref_service as irservice
from service import transaction_service
from service import macro_service
from service import table_service
from service import winners_list_service as wlservice
from strategys import common_strategy as cstg
from utils import util

logger = logging.getLogger(__name__)
today = util.get_today()
today_line = util.get_today_line()

yesterday = util.get_yesterday()
yesterday_line = util.get_yesterday_line()

tomorrow = util.get_tomorrow()
tomorrow_line = util.get_tomorrow_line()
QUARTERS = [1, 2, 3, 4]
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
    classfication_service.save_industry_classified()
    classfication_service.save_concept_classified()
    classfication_service.save_area_classified()
    classfication_service.save_sme_classified()
    classfication_service.save_gem_classified()
    classfication_service.save_st_classified()
    classfication_service.save_hs300s()
    classfication_service.save_sz50s()
    classfication_service.save_zz500s()
    classfication_service.save_terminated()
    classfication_service.save_suspend()
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


def strategy():
    cstg.macd_service()


def save_select_stocks_hist_data(start=None, end=None, ktype=None):
    """保存选择股票的交易数据"""
    
    stock_codes = ['600622']
    logger.info('Begin save select stocks history data')
    transaction_service.save_stocks_hist_data(stocks=stock_codes, start_date=start, end_date=end, ktype=ktype)
    logger.info('End save select stocks history data')


def save_select_stocks_h_data_revote(start=None, end=None, autype='qfp', index=False):
    stock_codes = ['600622']
    transaction_service.save_stock_h_data_revote(stocks=stock_codes, start_date=start,
                                                 end_date=end, autype=autype, index=index)


def args_parse():
    """参数解析"""

    parser = argparse.ArgumentParser(description='Get stock data with tushare')
    top_sub_parsers = parser.add_subparsers()
    parser.add_argument('-o', action='store_false', dest='need_open_date',
                        help='if need to judge with open data, default is true')

    # database table parser
    db_parser = top_sub_parsers.add_parser('d', help='database and table service')
    db_parser.add_argument('-da', action='store_true', dest='drop_tables', help='drop all tables')
    db_parser.add_argument('-ca', action='store_true', dest='create_tables', help='create all tables')
    db_parser.add_argument('-d', action='store_true', dest='drop_table',
                           help='drop tables, use with -t or --tables')
    db_parser.add_argument('-c', action='store_true', dest='create_table',
                           help='create tables, use with -t or --tables')
    db_parser.add_argument('-t', '--talbes', dest='tables', nargs='+',
                           help='create given tables, must be peewee model.')

    # transaction parser 交易数据
    transaction_parser = top_sub_parsers.add_parser('t', help='transaction service(交易数据)')
    transaction_parser.add_argument('-hk', action='store_true',
                                    dest='save_stocks_k_data',
                                    help='save stocks history k data, use with [--stocks, --start, --end, --ktype]')
    transaction_parser.add_argument('-hky', action='store_true',
                                    dest='save_yesterday_stocks_k_data',
                                    help='save yesterday stocks history k data, use with [--stocks, --ktype]')
    transaction_parser.add_argument('-hkt', action='store_true',
                                    dest='save_today_stocks_k_data',
                                    help='save today stocks history k data, use with [--stocks, --ktype]')
    transaction_parser.add_argument('-hi', action='store_true',
                                    dest='save_stocks_hist_data',
                                    help='save stocks history data, use with [--stocks, --start, --end, --ktype]')
    transaction_parser.add_argument('-hiy', action='store_true',
                                    dest='save_yesterday_stocks_history_data',
                                    help='save yesterday stocks history data, use with [--stocks, --ktype]')
    transaction_parser.add_argument('-hit', action='store_true',
                                    dest='save_today_stocks_history_data',
                                    help='save today stocks history data, use with [--stocks, --ktype]')
    transaction_parser.add_argument('-r', action='store_true',
                                    dest='save_stocks_revote_hist_data',
                                    help='save stocks revote history data, use with [--stocks, --start, --end]')
    transaction_parser.add_argument('-tad', action='store_true',
                                    dest='save_today_all_data',
                                    help='save today all stocks transaction data, if holidays, '
                                         'this is the last trade day data.')
    transaction_parser.add_argument('-tk', action='store_true',
                                    dest='save_tick_data',
                                    help='save tick data(获取历史的分笔数据明细), use with --date [, --stocks]')
    transaction_parser.add_argument('-tkr', action='store_true',
                                    dest='save_tick_data_range',
                                    help='save tick data date range(获取历史的分笔数据明细),'
                                         'use with [--stocks, --start, --end]')
    transaction_parser.add_argument('-ttk', action='store_true',
                                    dest='save_today_tick_data',
                                    help='save today tick data(获取当前交易日（当天六点后使用)), '
                                         'save_tick_data_range function be used, use with [--stocks]')
    transaction_parser.add_argument('-ttkt', action='store_true',
                                    dest='save_today_tick_data_while_trading',
                                    help='save today tick data while trading(获取当前交易日（交易中使用)), '
                                         'use with [--stocks]')
    transaction_parser.add_argument('-bi', action='store_true',
                                    dest='save_big_index_data',
                                    help='save big index data(获取大盘指数实时行情列表)')
    transaction_parser.add_argument('-bt', action='store_true',
                                    dest='save_big_trade_data',
                                    help='save big trade data(获取大单交易数据), use with [--date, --stocks]')
    transaction_parser.add_argument('-btr', action='store_true',
                                    dest='save_big_trade_data_range',
                                    help='save big trade data date range(获取大单交易数据), '
                                         'use with --start, --end [ ,--stocks]')

    transaction_parser.add_argument('-s', '--start', dest='start_date', help='start date,格式YYYY-MM-DD')
    transaction_parser.add_argument('-e', '--end', dest='end_date', help='end date,格式YYYY-MM-DD')
    transaction_parser.add_argument('-d', '--date', dest='date', help='date, the date wanted to be save,格式YYYY-MM-DD')
    transaction_parser.add_argument('--stocks', dest='stocks', nargs='+',
                                    help='stock codes which want to be deal.')
    transaction_parser.add_argument('-t', '--ktype', dest='ktype',
                                    help='数据类型: D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟',
                                    choices=['D', 'W', 'M', '5', '15', '30', '60'])
    # transaction_parser.add_argument('-a', action='store_true', dest='all_stocks', help='get all stocks data.')
    # transaction_parser.add_argument('-s', action='store_true', dest='select_stocks', help='get select stocks data.')

    # investment ref parser 投资参考数据
    investment_parser = top_sub_parsers.add_parser('i', help='investment ref service(投资参考数据)')
    investment_parser.add_argument('-d', action='store_true',
                                   dest='save_distribution_plans',
                                   help='save_distribution_plans(分配预案数据), use with [--year]')
    investment_parser.add_argument('-p', action='store_true',
                                   dest='save_performance_forecast',
                                   help='save_performance_forecast(业绩预告), use with [--quarter, --year]')
    investment_parser.add_argument('-r', action='store_true',
                                   dest='save_restricted_stock',
                                   help='save_restricted_stock(限售股解禁数据), use with [--year, --month]')
    investment_parser.add_argument('-fh', action='store_true',
                                   dest='save_fund_holdings',
                                   help='save_fund_holdings(基金持股), use with [--quarter, --year]')
    investment_parser.add_argument('-n', action='store_true',
                                   dest='save_new_stocks',
                                   help='save_new_stocks(新股持股)')
    investment_parser.add_argument('-fsh', action='store_true',
                                   dest='save_financing_securities_sh',
                                   help='save_financing_securities_sh(融资融券（沪市)), use with [--start, --end]')
    investment_parser.add_argument('-fsdh', action='store_true',
                                   dest='save_financing_securities_detail_sh',
                                   help='save_financing_securities_detail_sh(沪市融资融券明细数据), '
                                        'use with [--date, --start, --end]')
    investment_parser.add_argument('-fsz', action='store_true',
                                   dest='save_financing_securities_sz',
                                   help='save_financing_securities_sz(融资融券（深市)), use with [--start, --end]')
    investment_parser.add_argument('-fsdz', action='store_true',
                                   dest='save_financing_securities_detail_sz',
                                   help='save_financing_securities_detail_sz(深市融资融券明细数据), use with --date')

    investment_parser.add_argument('-y', '--year', dest='year', type=int, help='年份')
    investment_parser.add_argument('-m', '--month', dest='month', type=int, help='月份',
                                   choices=xrange(1, 13))
    investment_parser.add_argument('-q', '--quarter', dest='quarter', type=int, help='季度',
                                   choices=[1, 2, 3, 4])

    # classified parser 股票分类数据
    classified_parser = top_sub_parsers.add_parser('c', help='classified service(股票分类数据)')
    classified_parser.add_argument('-i', action='store_true',
                                   dest='save_industry_classified',
                                   help='save_industry_classified(行业分类)')
    classified_parser.add_argument('-c', action='store_true',
                                   dest='save_concept_classified',
                                   help='save_concept_classified(股票概念分类)')
    classified_parser.add_argument('-a', action='store_true',
                                   dest='save_area_classified',
                                   help='save_area_classified(地域分类)')
    classified_parser.add_argument('-s', action='store_true',
                                   dest='save_sme_classified',
                                   help='save_sme_classified(中小板分类)')
    classified_parser.add_argument('-g', action='store_true',
                                   dest='save_gem_classified',
                                   help='save_gem_classified(创业板分类)')
    classified_parser.add_argument('-st', action='store_true',
                                   dest='save_st_classified',
                                   help='save_st_classified(风险警示板块)')
    classified_parser.add_argument('-hs', action='store_true',
                                   dest='save_hs300s',
                                   help='save_hs300s(沪深300成分股所占权重)')
    classified_parser.add_argument('-sz', action='store_true',
                                   dest='save_sz50s',
                                   help='save_sz50s(上证50成分股)')
    classified_parser.add_argument('-zz', action='store_true',
                                   dest='save_zz500s',
                                   help='save_zz500s(中证500成分股)')
    classified_parser.add_argument('-t', action='store_true',
                                   dest='save_terminated',
                                   help='save_terminated(终止上市股票列表)')
    classified_parser.add_argument('-sp', action='store_true',
                                   dest='save_suspend',
                                   help='save_suspend(暂停上市的股票列表)')

    # base parser 基本面数据
    base_parser = top_sub_parsers.add_parser('b', help='base service(基本面数据)')
    base_parser.add_argument('-s', action='store_true',
                             dest='save_stocks_basic_data',
                             help='save_stocks_basic_data(股票列表)')
    base_parser.add_argument('-pr', action='store_true',
                             dest='save_performance_report',
                             help='save_performance_report(业绩报告(主表)), use with --quarter [, --year]')
    base_parser.add_argument('-pa', action='store_true',
                             dest='save_profit_ability',
                             help='save_profit_ability(盈利能力), use with --quarter [, --year]')
    base_parser.add_argument('-oa', action='store_true',
                             dest='save_operation_ability',
                             help='save_operation_ability(营运能力), use with --quarter [, --year]')
    base_parser.add_argument('-ga', action='store_true',
                             dest='save_growth_ability',
                             help='save_growth_ability(成长能力), use with --quarter [, --year]')
    base_parser.add_argument('-pd', action='store_true',
                             dest='save_pay_debt_ability',
                             help='save_pay_debt_ability(偿债能力), use with --quarter [, --year]')
    base_parser.add_argument('-c', action='store_true',
                             dest='save_cash_flow',
                             help='save_cash_flow(现金流量), use with --quarter [, --year]')

    base_parser.add_argument('-y', '--year', dest='year', type=int, help='年份')
    base_parser.add_argument('-q', '--quarter', dest='quarter', type=int, help='季度',
                             choices=[1, 2, 3, 4])
    base_parser.add_argument('-d', '--date', dest='date', help='date, the date wanted to be save,格式YYYY-MM-DD')

    # macro parser 宏观经济数据
    macro_parser = top_sub_parsers.add_parser('m', help='macro service(宏观经济数据)')
    macro_parser.add_argument('-r', action='store_true',
                              dest='save_required_reserves_rate',
                              help='save_required_reserves_rate(存款准备金率)')
    macro_parser.add_argument('-ms', action='store_true',
                              dest='save_money_supply',
                              help='save_money_supply(货币供应量)')
    macro_parser.add_argument('-msb', action='store_true',
                              dest='save_money_supply_bal',
                              help='save_money_supply_bal(货币供应量(年底余额))')
    macro_parser.add_argument('-gy', action='store_true',
                              dest='save_gdp_year',
                              help='save_gdp_year(国内生产总值(年度))')
    macro_parser.add_argument('-gq', action='store_true',
                              dest='save_gdp_quarter',
                              help='save_gdp_quarter(得到国内生产总值(季度))')
    macro_parser.add_argument('-gd', action='store_true',
                              dest='save_gdp_three_demands',
                              help='save_gdp_three_demands(三大需求对GDP贡献)')
    macro_parser.add_argument('-gip', action='store_true',
                              dest='save_gdp_three_industry_pull',
                              help='save_gdp_three_industry_pull(三大产业对GDP拉动)')
    macro_parser.add_argument('-gic', action='store_true',
                              dest='save_gdp_three_industry_contrib',
                              help='save_gdp_three_industry_contrib(三大产业贡献率)')
    macro_parser.add_argument('-c', action='store_true',
                              dest='save_cpi',
                              help='save_cpi(居民消费价格指数)')
    macro_parser.add_argument('-p', action='store_true',
                              dest='save_ppi',
                              help='save_ppi(工业品出厂价格指数)')

    # winners parser 龙虎榜数据
    winners_parser = top_sub_parsers.add_parser('w', help='macro service(龙虎榜数据)')
    winners_parser.add_argument('-t', action='store_true', dest='save_top_list',
                                help='save_top_list(每日龙虎榜列表), use with -d')
    winners_parser.add_argument('-is', action='store_true', dest='save_individual_statistics_tops',
                                help='save_individual_statistics_tops(个股上榜统计), use with [-dt]')
    winners_parser.add_argument('-b', action='store_true', dest='save_broker_tops',
                                help='save_broker_tops(营业部上榜统计), use with [-dt]')
    winners_parser.add_argument('-it', action='store_true', dest='save_institution_tops',
                                help='save_institution_tops(机构席位追踪), use with [-dt]')
    winners_parser.add_argument('-id', action='store_true', dest='save_institution_detail',
                                help='save_institution_detail(机构成交明细)')

    winners_parser.add_argument('-d', '--date', dest='date', help='date日期,格式YYYY-MM-DD')
    winners_parser.add_argument('-dt', '--days_type', dest='days_type', type=int,
                                nargs='+', choices=[5, 10, 30, 60],
                                help='统计周期5、10、30和60日，为空时保存所有的这几个类型')

    # bank loan parser  银行间同业拆放利率
    bank_loan_parser = top_sub_parsers.add_parser('l', help='bank loan service(银行间同业拆放利率)')
    bank_loan_parser.add_argument('-r', action='store_true', dest='save_shibor_rate',
                                  help='save_shibor_rate(上海银行间同业拆放利率), use with [-y or --year]')
    bank_loan_parser.add_argument('-q', action='store_true', dest='save_shibor_quote',
                                  help='save_shibor_quote(银行报价数据), use with [-y or --year]')
    bank_loan_parser.add_argument('-m', action='store_true', dest='save_shibor_ma',
                                  help='save_shibor_ma(Shibor均值数据), use with [-y or --year]')
    bank_loan_parser.add_argument('-l', action='store_true', dest='save_lpr',
                                  help='save_lpr(贷款基础利率), use with [-y or --year]')
    bank_loan_parser.add_argument('-lm', action='store_true', dest='save_lpr_ma',
                                  help='save_lpr_ma(贷款基础利率均值数据), use with [-y or --year]')

    bank_loan_parser.add_argument('-y', '--year', dest='year', type=int, help='年份')

    _args = parser.parse_args()
    logger.debug(_args)
    return _args


def main():
    import tushare as ts

    args = args_parse()
    logger.info('Args is: %s.' % args)
    if args.need_open_date:
        dates = ts.trade_cal()
        is_open = dates[dates.calendarDate == today_line].query('isOpen==0').empty
        if not is_open:
            logger.info('Today is not open date, so do nothing.')
            sys.exit(-1)

    # transaction 交易数据
    if hasattr(args, 'save_stocks_k_data') and args.save_stocks_k_data:
        transaction_service.save_stocks_k_data(stocks=args.stocks, start_date=args.start_date,
                                               end_date=args.end_date, ktype=args.ktype)
    if hasattr(args, 'save_yesterday_stocks_k_data') and args.save_yesterday_stocks_k_data:
        transaction_service.save_yesterday_stocks_k_data(stocks=args.stocks, ktype=args.ktype)
    if hasattr(args, 'save_today_stocks_k_data') and args.save_today_stocks_k_data:
        transaction_service.save_today_stocks_k_data(stocks=args.stocks, ktype=args.ktype)
    if hasattr(args, 'save_stocks_hist_data') and args.save_stocks_hist_data:
        transaction_service.save_stocks_hist_data(stocks=args.stocks, start_date=args.start_date,
                                                  end_date=args.end_date, ktype=args.ktype)
    if hasattr(args, 'save_yesterday_stocks_history_data') and args.save_yesterday_stocks_history_data:
        transaction_service.save_yesterday_stocks_hist_data(stocks=args.stocks, ktype=args.ktype)
    if hasattr(args, 'save_today_stocks_history_data') and args.save_today_stocks_history_data:
        transaction_service.save_today_stocks_hist_data(stocks=args.stocks, ktype=args.ktype)
    if hasattr(args, 'save_stocks_revote_hist_data') and args.save_stocks_revote_hist_data:
        transaction_service.save_stock_h_data_revote(stocks=args.stocks, start_date=args.start_date,
                                                     end_date=args.end_date)
    if hasattr(args, 'save_today_all_data') and args.save_today_all_data:
        transaction_service.save_today_all_data()
    if hasattr(args, 'save_tick_data') and args.save_tick_data:
        transaction_service.save_tick_data(date=args.date, stocks=args.stocks)
    if hasattr(args, 'save_tick_data_range') and args.save_tick_data_range:
        transaction_service.save_tick_data_range(start_date=args.start_date,
                                                 end_date=args.end_date, stocks=args.stocks)
    if hasattr(args, 'save_today_tick_data') and args.save_today_tick_data:
        transaction_service.save_today_tick_data(stocks=args.stocks)
    if hasattr(args, 'save_today_tick_data_while_trading') and args.save_today_tick_data_while_trading:
        transaction_service.save_today_tick_data_while_trading(stocks=args.stocks)
    if hasattr(args, 'save_big_index_data') and args.save_big_index_data:
        transaction_service.save_big_index_data()
    if hasattr(args, 'save_big_trade_data') and args.save_big_trade_data:
        transaction_service.save_big_trade_data(date=args.date, stocks=args.stocks)
    if hasattr(args, 'save_big_trade_data_range') and args.save_big_trade_data_range:
        transaction_service.save_big_trade_data_range(start_date=args.start_date,
                                                      end_date=args.end_date, stocks=args.stocks)

    # investment ref  投资参考数据
    if hasattr(args, 'save_distribution_plans') and args.save_distribution_plans:
        irservice.save_distribution_plans(year=args.year)
    if hasattr(args, 'save_performance_forecast') and args.save_performance_forecast:
        irservice.save_performance_forecast(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_restricted_stock') and args.save_restricted_stock:
        irservice.save_restricted_stock(year=args.year, month=args.month)
    if hasattr(args, 'save_fund_holdings') and args.save_fund_holdings:
        irservice.save_fund_holdings(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_new_stocks') and args.save_new_stocks:
        irservice.save_new_stocks()
    if hasattr(args, 'save_financing_securities_sh') and args.save_financing_securities_sh:
        irservice.save_financing_securities_sh(start_date=args.start_date, end_date=args.end_date)
    if hasattr(args, 'save_financing_securities_detail_sh') and args.save_financing_securities_detail_sh:
        irservice.save_financing_securities_detail_sh(date=args.date,
                                                      start_date=args.start_date, end_date=args.end_date)
    if hasattr(args, 'save_financing_securities_sz') and args.save_financing_securities_sz:
        irservice.save_financing_securities_sz(start_date=args.start_date, end_date=args.end_date)
    if hasattr(args, 'save_financing_securities_detail_sz') and args.save_financing_securities_detail_sz:
        irservice.save_financing_securities_detail_sz(date=args.date)

    # classified  股票分类数据
    if hasattr(args, 'save_industry_classified') and args.save_industry_classified:
        classfication_service.save_industry_classified()
    if hasattr(args, 'save_concept_classified') and args.save_concept_classified:
        classfication_service.save_concept_classified()
    if hasattr(args, 'save_area_classified') and args.save_area_classified:
        classfication_service.save_area_classified()
    if hasattr(args, 'save_sme_classified') and args.save_sme_classified:
        classfication_service.save_sme_classified()
    if hasattr(args, 'save_gem_classified') and args.save_gem_classified:
        classfication_service.save_gem_classified()
    if hasattr(args, 'save_st_classified') and args.save_st_classified:
        classfication_service.save_st_classified()
    if hasattr(args, 'save_hs300s') and args.save_hs300s:
        classfication_service.save_hs300s()
    if hasattr(args, 'save_sz50s') and args.save_sz50s:
        classfication_service.save_sz50s()
    if hasattr(args, 'save_zz500s') and args.save_zz500s:
        classfication_service.save_zz500s()
    if hasattr(args, 'save_terminated') and args.save_terminated:
        classfication_service.save_terminated()
    if hasattr(args, 'save_suspend') and args.save_suspend:
        classfication_service.save_suspend()

    # base parser 基本面数据
    if hasattr(args, 'save_stocks_basic_data') and args.save_stocks_basic_data:
        base_service.save_stocks_basic_data(args.date)
    if hasattr(args, 'save_performance_report') and args.save_performance_report:
        quarter = args.quarter
        if quarter is None:
            for quarter in QUARTERS:
                base_service.save_performance_report(year=args.year, quarter=quarter)
        else:
            base_service.save_performance_report(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_profit_ability') and args.save_profit_ability:
        quarter = args.quarter
        if quarter is None:
            for quarter in QUARTERS:
                base_service.save_profit_ability(year=args.year, quarter=quarter)
        else:
            base_service.save_profit_ability(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_operation_ability') and args.save_operation_ability:
        quarter = args.quarter
        if quarter is None:
            for quarter in QUARTERS:
                base_service.save_operation_ability(year=args.year, quarter=quarter)
        else:
            base_service.save_operation_ability(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_growth_ability') and args.save_growth_ability:
        quarter = args.quarter
        if quarter is None:
            for quarter in QUARTERS:
                base_service.save_growth_ability(year=args.year, quarter=quarter)
        else:
            base_service.save_growth_ability(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_pay_debt_ability') and args.save_pay_debt_ability:
        quarter = args.quarter
        if quarter is None:
            for quarter in QUARTERS:
                base_service.save_pay_debt_ability(year=args.year, quarter=quarter)
        else:
            base_service.save_pay_debt_ability(year=args.year, quarter=args.quarter)
    if hasattr(args, 'save_cash_flow') and args.save_cash_flow:
        quarter = args.quarter
        if quarter is None:
            for quarter in QUARTERS:
                base_service.save_cash_flow(year=args.year, quarter=quarter)
        else:
            base_service.save_cash_flow(year=args.year, quarter=args.quarter)

    # macro 宏观经济数据
    if hasattr(args, 'save_required_reserves_rate') and args.save_required_reserves_rate:
        macro_service.save_required_reserves_rate()
    if hasattr(args, 'save_money_supply') and args.save_money_supply:
        macro_service.save_money_supply()
    if hasattr(args, 'save_money_supply_bal') and args.save_money_supply_bal:
        macro_service.save_money_supply_bal()
    if hasattr(args, 'save_gdp_year') and args.save_gdp_year:
        macro_service.save_gdp_year()
    if hasattr(args, 'save_gdp_quarter') and args.save_gdp_quarter:
        macro_service.save_gdp_quarter()
    if hasattr(args, 'save_gdp_three_demands') and args.save_gdp_three_demands:
        macro_service.save_gdp_three_demands()
    if hasattr(args, 'save_gdp_three_industry_pull') and args.save_gdp_three_industry_pull:
        macro_service.save_gdp_three_industry_pull()
    if hasattr(args, 'save_gdp_three_industry_contrib') and args.save_gdp_three_industry_contrib:
        macro_service.save_gdp_three_industry_contrib()
    if hasattr(args, 'save_cpi') and args.save_cpi:
        macro_service.save_cpi()
    if hasattr(args, 'save_ppi') and args.save_ppi:
        macro_service.save_ppi()

    # winners 龙虎榜数据
    if hasattr(args, 'save_top_list') and args.save_top_list:
        wlservice.save_top_list(date=args.date)
    if hasattr(args, 'save_individual_statistics_tops') and args.save_individual_statistics_tops:
        wlservice.save_individual_statistics_tops(days_type=args.days_type)
    if hasattr(args, 'save_broker_tops') and args.save_broker_tops:
        wlservice.save_broker_tops(days_type=args.days_type)
    if hasattr(args, 'save_institution_tops') and args.save_institution_tops:
        wlservice.save_institution_tops(days_type=args.days_type)
    if hasattr(args, 'save_institution_detail') and args.save_institution_detail:
        wlservice.save_institution_detail()

    # bank loan 银行间同业拆放利率
    if hasattr(args, 'save_shibor_rate') and args.save_shibor_rate:
        blservice.save_shibor_rate(year=args.year)
    if hasattr(args, 'save_shibor_quote') and args.save_shibor_quote:
        blservice.save_shibor_quote(year=args.year)
    if hasattr(args, 'save_shibor_ma') and args.save_shibor_ma:
        blservice.save_shibor_ma(year=args.year)
    if hasattr(args, 'save_lpr') and args.save_lpr:
        blservice.save_lpr(year=args.year)
    if hasattr(args, 'save_lpr_ma') and args.save_lpr_ma:
        blservice.save_lpr_ma(year=args.year)

    # database and table
    if hasattr(args, 'drop_tables') and args.drop_tables:
        table_service.drop_all_tables()
    if hasattr(args, 'create_tables') and args.create_tables:
        table_service.create_all_tables()
    # database and table
    if hasattr(args, 'drop_table') and args.drop_table:
        table_service.drop_tables(args.tables)
    if hasattr(args, 'create_table') and args.create_table:
        table_service.create_tables(args.tables)


if __name__ == '__main__':
    setup_logging()
    main()
