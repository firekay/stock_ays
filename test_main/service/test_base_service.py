# encoding: UTF-8
from service import base_service
from test_main.constants import *
import test_main


def test_save_performance_report():
    base_service.save_performance_report(YEAR, QUARTER)


def test_save_stocks_basic_data():
    base_service.save_stocks_basic_data()

if __name__ == '__main__':
    test_main.setup_logging()
    test_save_stocks_basic_data()
    # test_save_performance_report()
