# encoding: utf-8
import logging
from dal import investment_ref_dal as irdal
from models.model import *
from dal import util_dal
from utils import util

logger = logging.getLogger(__name__)
QUARTERS = [1, 2, 3, 4]


def save_distribution_plans(year=None, top=5000):
    """得到分配预案数据
    
    Args:
        year : 预案公布的年份，默认为2014
        top :取最新n条数据，默认取最近公布的5000条
    """
    year = util.get_year() if year is None else year
    data_dicts = irdal.get_distribution_plans_data(year, top)
    if data_dicts:
        if util_dal.delete_year_data(DistributionPlans, year):
            irdal.save_distribution_plans_data(data_dicts, year)


def save_performance_forecast(year, quarter):
    """业绩预告
    
    Args:
        year: 年份
        quarter: 季度, 默认删除给定年份的所有季度数据
    """
    year = util.get_year() if year is None else year
    if quarter is None:
        for quarter in QUARTERS:
            data_dicts = irdal.get_performance_forecast(year, quarter)
            if data_dicts:
                if util_dal.delete_year_quarter_data(PerformanceForecast, year, quarter):
                    util_dal.save_year_quarter_data(PerformanceForecast, data_dicts, year, quarter)
    else:
        data_dicts = irdal.get_performance_forecast(year, quarter)
        if data_dicts:
            if util_dal.delete_year_quarter_data(PerformanceForecast, year, quarter):
                util_dal.save_year_quarter_data(PerformanceForecast, data_dicts, year, quarter)


def save_restricted_stock(year=None, month=None):
    """ 限售股解禁数据
    
    Args
        year:年份,默认为当前年
        month:解禁月份，默认为当前月
    """
    year = util.get_year() if year is None else year
    month = util.get_month() if month is None else month
    data_dicts = irdal.get_restricted_stock(year, month)
    if data_dicts:
        if util_dal.delete_year_month_data(RestrictedStock, year, month):
            util_dal.save_year_month_data(RestrictedStock, data_dicts, year, month)


def save_fund_holdings(year, quarter):
    """基金持股
    Args:
        year: 年份
        quarter: 季度, 默认删除给定年份的所有季度数据
    """
    year = util.get_year() if year is None else year
    if quarter is None:
        for quarter in QUARTERS:
            data_dicts = irdal.get_fund_holdings(year, quarter)
            if data_dicts:
                if util_dal.delete_year_quarter_data(FundHoldings, year, quarter):
                    util_dal.save_year_quarter_data(FundHoldings, data_dicts, year, quarter)
    else:
        data_dicts = irdal.get_fund_holdings(year, quarter)
        if data_dicts:
            if util_dal.delete_year_quarter_data(FundHoldings, year, quarter):
                util_dal.save_year_quarter_data(FundHoldings, data_dicts, year, quarter)


def save_new_stocks():
    """新股数据"""
    data_dicts = irdal.NewStocksDal.get_new_stocks()
    if data_dicts:
        irdal.NewStocksDal.save_new_stocks(data_dicts)


def save_financing_securities_sh(start_date=None, end_date=None):
    """融资融券（沪市)
    
    Args:
        start_date: 开始日期 format：YYYY-MM-DD 为空时取去年今日
        end_date: 结束日期 format：YYYY-MM-DD 为空时取当前日期
    """
    data_dicts = irdal.FinancingSecuritiesShDal.get_financing_securities_sh(start_date, end_date)
    if data_dicts:
        irdal.FinancingSecuritiesShDal.save_financing_securities_sh(data_dicts)


def save_financing_securities_detail_sh(date=None, start_date=None, end_date=None):
    """沪市融资融券明细数据
    
    Args:
        start_date: 开始日期 format：YYYY-MM-DD 默认为空’‘, 
                    如过end_date为空, 则只取start_date这一天数据
        end_date: 结束日期 format：YYYY-MM-DD 默认为空’‘
    """
    # 如果end_date为None, 则只有start_date一天的的数据
    data_dicts = irdal.FinancingSecuritiesDetailShDal.get_financing_securities_detail_sh(start_date=start_date,
                                                                                         end_date=end_date)
    if data_dicts:
        if irdal.FinancingSecuritiesDetailShDal.delete_some_days_data(date=date, start_date=start_date,
                                                                      end_date=end_date):
            irdal.FinancingSecuritiesDetailShDal.save_financing_securities_detail_sh(data_dicts, date=date,
                                                                                     start_date=start_date,
                                                                                     end_date=end_date)


def save_financing_securities_sz(start_date=None, end_date=None):
    """融资融券（深市)
    
    Args:
        start_date: 开始日期 format：YYYY-MM-DD 为空时取去年今日
        end_date: 结束日期 format：YYYY-MM-DD 为空时取当前日期
    """
    data_dicts = irdal.FinancingSecuritiesSzDal.get_financing_securities_sz(start_date, end_date)
    if data_dicts:
        irdal.FinancingSecuritiesSzDal.save_financing_securities_sz(data_dicts)


def save_financing_securities_detail_sz(date):
    """深市融资融券明细数据 """
    date = util.get_last_trading_day(date)
    data_dicts = irdal.FinancingSecuritiesDetailSzDal.get_financing_securities_detail_sz(date=date)
    if data_dicts:
        if irdal.FinancingSecuritiesDetailSzDal.delete_some_day_data(date=date):
            irdal.FinancingSecuritiesDetailSzDal.save_financing_securities_detail_sz(data_dicts, date=date)
