# encoding: UTF-8
import test_main
from service import investment_ref_service as irservice
from test_main.service.constants import *


def test_save_distribution_plans():
    irservice.save_distribution_plans(YEAR)


def test_save_restricted_stock():
    irservice.save_restricted_stock(YEAR, MONTH)


def test_save_performance_forecast():
    irservice.save_performance_forecast(YEAR, QUARTER)


def test_save_restricted_stock():
    irservice.save_restricted_stock()


def test_save_fund_holdings():
    irservice.save_fund_holdings(YEAR, QUARTER)


def test_save_new_stocks():
    irservice.save_new_stocks()


def test_save_financing_securities_sh():
    irservice.save_financing_securities_sh()


def test_save_financing_securities_detail_sh():
    irservice.save_financing_securities_detail_sh(TODAY_LINE)


def test_save_financing_securities_sz():
    irservice.save_financing_securities_sz()


def test_save_financing_securities_detail_sz():
    irservice.save_financing_securities_detail_sz(TODAY_LINE)


if __name__ == '__main__':
    test_main.setup_logging()
    test_save_distribution_plans()
    test_save_restricted_stock()
    test_save_performance_forecast()
    test_save_restricted_stock()
    test_save_fund_holdings()
    test_save_new_stocks()
    test_save_financing_securities_sh()
    test_save_financing_securities_detail_sh()
    test_save_financing_securities_sz()
    test_save_financing_securities_detail_sz()

