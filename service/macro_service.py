# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import macro_dal
from dal import util_dal

logger = logging.getLogger(__name__)


def save_deposit_rate():
    """得到存款利率"""
    table_service.truncate_table(DepositsRate)
    data_dicts = macro_dal.get_deposit_rate()
    if data_dicts:
        util_dal.save_data(DepositsRate, data_dicts)


def save_loan_rate():
    """得到贷款利率"""
    table_service.truncate_table(LoanRate)
    data_dicts = macro_dal.get_loan_rate()
    if data_dicts:
        util_dal.save_data(LoanRate, data_dicts)


def save_required_reserves_rate():
    """得到存款准备金率"""
    table_service.truncate_table(RequiredReservesRate)
    data_dicts = macro_dal.get_required_reserves_rate()
    if data_dicts:
        util_dal.save_data(RequiredReservesRate, data_dicts)


def save_money_supply():
    """得到货币供应量"""
    table_service.truncate_table(MoneySupply)
    data_dicts = macro_dal.get_money_supply()
    if data_dicts:
        util_dal.save_data(MoneySupply, data_dicts)


def save_money_supply_bal():
    """得到货币供应量(年底余额)"""
    table_service.truncate_table(MoneySupplyBal)
    data_dicts = macro_dal.get_money_supply_bal()
    if data_dicts:
        util_dal.save_data(MoneySupplyBal, data_dicts)


def save_gdp_year():
    """国内生产总值(年度)"""
    table_service.truncate_table(GrossDomesticProductYear)
    data_dicts = macro_dal.get_gdp_year()
    if data_dicts:
        util_dal.save_data(GrossDomesticProductYear, data_dicts)


def save_gdp_quarter():
    """得到国内生产总值(季度)"""
    table_service.truncate_table(GrossDomesticProductQuarter)
    data_dicts = macro_dal.get_gdp_quarter()
    if data_dicts:
        util_dal.save_data(GrossDomesticProductQuarter, data_dicts)


def save_gdp_three_demands():
    """三大需求对GDP贡献"""
    table_service.truncate_table(GdpThreeDemands)
    data_dicts = macro_dal.get_gdp_three_demands()
    if data_dicts:
        util_dal.save_data(GdpThreeDemands, data_dicts)


def save_gdp_three_industry_pull():
    """三大产业对GDP拉动"""
    table_service.truncate_table(GdpThreeIndustryPull)
    data_dicts = macro_dal.get_gdp_three_industry_pull()
    if data_dicts:
        util_dal.save_data(GdpThreeIndustryPull, data_dicts)


def save_gdp_three_industry_contrib():
    """三大产业贡献率"""
    table_service.truncate_table(GdpThreeIndustryContrib)
    data_dicts = macro_dal.get_gdp_three_industry_contrib()
    if data_dicts:
        util_dal.save_data(GdpThreeIndustryContrib, data_dicts)


def save_cpi():
    """居民消费价格指数"""
    table_service.truncate_table(CPI)
    data_dicts = macro_dal.get_cpi()
    if data_dicts:
        util_dal.save_data(CPI, data_dicts)


def save_ppi():
    """工业品出厂价格指数"""
    table_service.truncate_table(PPI)
    data_dicts = macro_dal.get_ppi()
    if data_dicts:
        util_dal.save_data(PPI, data_dicts)
