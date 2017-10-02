# encoding: UTF-8
""""""

from models.model import *
from dal import bank_loan_call_rate_dal as bankl_dal
from dal import util_dal


def save_shibor_rate(year=None):
    data_dicts = bankl_dal.get_shibor_rate(year)
    if data_dicts:
        if util_dal.delete_year(ShiborRate, year):
            util_dal.save_data(ShiborRate, year)


def save_shibor_quote(year=None):
    data_dicts = bankl_dal.get_shibor_quote(year)
    if data_dicts:
        if util_dal.delete_year(ShiborQuote, year):
            util_dal.save_data(ShiborQuote, year)


def save_shibor_ma(year=None):
    data_dicts = bankl_dal.get_shibor_ma(year)
    if data_dicts:
        if util_dal.delete_year(ShiborMA, year):
            util_dal.save_data(ShiborMA, year)


def save_lpr(year=None):
    data_dicts = bankl_dal.get_lpr(year)
    if data_dicts:
        if util_dal.delete_year(LPR, year):
            util_dal.save_data(LPR, year)


def save_lpr_ma(year=None):
    data_dicts = bankl_dal.get_lpr_ma(year)
    if data_dicts:
        if util_dal.delete_year(LprMA, year):
            util_dal.save_data(LprMA, year)
