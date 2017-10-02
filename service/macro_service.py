# encoding: UTF-8
""""""

import logging
from models.model import *
from service import table_service
from dal import macro_dal
from dal import util_dal

logger = logging.getLogger(__name__)


def save_deposit_rate():
    table_service.truncate_table(DepositsRate)
    data_dicts = macro_dal.get_deposit_rate()
    if data_dicts:
        util_dal.save_data(DepositsRate, data_dicts)


def save_loan_rate():
    table_service.truncate_table(LoanRate)
    data_dicts = macro_dal.get_loan_rate()
    if data_dicts:
        util_dal.save_data(LoanRate, data_dicts)


def save_required_reserves_rate():
    table_service.truncate_table(RequiredReservesRate)
    data_dicts = macro_dal.get_required_reserves_rate()
    if data_dicts:
        util_dal.save_data(RequiredReservesRate, data_dicts)


def save_money_supply():
    table_service.truncate_table(MoneySupply)
    data_dicts = macro_dal.get_money_supply()
    if data_dicts:
        util_dal.save_data(MoneySupply, data_dicts)


def save_money_supply_bal():
    table_service.truncate_table(MoneySupplyBal)
    data_dicts = macro_dal.get_money_supply_bal()
    if data_dicts:
        util_dal.save_data(MoneySupplyBal, data_dicts)


def save_gdp_year():
    table_service.truncate_table(GrossDomesticProductYear)
    data_dicts = macro_dal.get_gdp_year()
    if data_dicts:
        util_dal.save_data(GrossDomesticProductYear, data_dicts)


def save_gdp_quarter():
    table_service.truncate_table(GrossDomesticProductQuarter)
    data_dicts = macro_dal.get_gdp_quarter()
    if data_dicts:
        util_dal.save_data(GrossDomesticProductQuarter, data_dicts)


def save_gdp_three_demands():
    table_service.truncate_table(GdpThreeDemands)
    data_dicts = macro_dal.get_gdp_three_demands()
    if data_dicts:
        util_dal.save_data(GdpThreeDemands, data_dicts)


def save_gdp_three_industry_pull():
    table_service.truncate_table(GdpThreeIndustryPull)
    data_dicts = macro_dal.get_gdp_three_industry_pull()
    if data_dicts:
        util_dal.save_data(GdpThreeIndustryPull, data_dicts)


def save_gdp_three_industry_contrib():
    table_service.truncate_table(GdpThreeIndustryContrib)
    data_dicts = macro_dal.get_gdp_three_industry_contrib()
    if data_dicts:
        util_dal.save_data(GdpThreeIndustryContrib, data_dicts)


def save_cpi():
    table_service.truncate_table(CPI)
    data_dicts = macro_dal.get_cpi()
    if data_dicts:
        util_dal.save_data(CPI, data_dicts)


def save_ppi():
    table_service.truncate_table(PPI)
    data_dicts = macro_dal.get_ppi()
    if data_dicts:
        util_dal.save_data(PPI, data_dicts)
