# encoding: UTF-8
""""""

from models.model import *
from dal import bank_loan_call_rate_dal as bankl_dal
from dal import util_dal


def save_shibor_rate(year=None):
    """上海银行间同业拆放利率（Shanghai Interbank Offered Rate，简称Shibor）
    
    Args:
        year: 年份(YYYY),默认为当前年份
    """
    data_dicts = bankl_dal.get_shibor_rate(year)
    if data_dicts:
        if util_dal.delete_year_data(ShiborRate, year):
            util_dal.save_year_data(ShiborRate, data_dicts, year)


def save_shibor_quote(year=None):
    """银行报价数据

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    data_dicts = bankl_dal.get_shibor_quote(year)
    if data_dicts:
        if util_dal.delete_year_data(ShiborQuote, year):
            util_dal.save_year_data(ShiborQuote, data_dicts, year)


def save_shibor_ma(year=None):
    """Shibor均值数据（Shanghai Interbank Offered Rate，简称Shibor）

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    data_dicts = bankl_dal.get_shibor_ma(year)
    if data_dicts:
        if util_dal.delete_year_data(ShiborMA, year):
            util_dal.save_year_data(ShiborMA, data_dicts, year)


def save_lpr(year=None):
    """贷款基础利率（LPR）（Shanghai Interbank Offered Rate，简称Shibor）

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    data_dicts = bankl_dal.get_lpr(year)
    if data_dicts:
        if util_dal.delete_year_data(LPR, year):
            util_dal.save_year_data(LPR, data_dicts, year)


def save_lpr_ma(year=None):
    """上海银行间同业拆放利率（Shanghai Interbank Offered Rate，简称Shibor）

    Args:
        year: 年份(YYYY),默认为当前年份
    """
    data_dicts = bankl_dal.get_lpr_ma(year)
    if data_dicts:
        if util_dal.delete_year_data(LprMA, year):
            util_dal.save_year_data(LprMA, data_dicts, year)
