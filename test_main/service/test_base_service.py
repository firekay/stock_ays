# encoding: UTF-8
from service import base_service
from test_main.constants import *
from utils import util
import test_main


def test_save_stocks_basic_data():
    base_service.save_stocks_basic_data()


def test_get_max_stock(insert_date):
    print base_service.get_max_stock(insert_date)


def test_save_performance_report():
    base_service.save_performance_report(YEAR, QUARTER)


def test_save_profit_ability():
    base_service.save_profit_ability(YEAR, QUARTER)


def test_save_operation_ability():
    base_service.save_operation_ability(YEAR, QUARTER)


def test_save_growth_ability():
    base_service.save_growth_ability(YEAR, QUARTER)


def test_save_pay_debt_ability():
    base_service.save_pay_debt_ability(YEAR, QUARTER)


def test_load_stocks_before_entering_date():
    stocks = base_service.load_stocks_before_entering_date('20170701', util.get_today_line())
    print(stocks.count())


def test_save_cash_flow():
    base_service.save_cash_flow(YEAR, QUARTER)


if __name__ == '__main__':
    test_load_stocks_before_entering_date()

    # test_main.setup_logging()
    # test_get_max_stock(util.get_today_line())
    # test_save_stocks_basic_data()
    # test_save_performance_report()
    # test_save_profit_ability()
    # test_save_operation_ability()
    # test_save_growth_ability()
    # test_save_pay_debt_ability()
    # test_save_cash_flow()
