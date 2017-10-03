# encoding: UTF-8
from service import bank_loan_call_rate_service as blservice
import test_main
from test_main.constants import *


def test_save_shibor_rate():
    blservice.save_shibor_rate(YEAR)


def test_save_shibor_quote():
    blservice.save_shibor_quote(YEAR)


def test_save_shibor_ma():
    blservice.save_shibor_ma(YEAR)


def test_save_lpr():
    blservice.save_lpr(YEAR)


def test_save_lpr_ma():
    blservice.save_lpr_ma(YEAR)


if __name__ == '__main__':
    test_main.setup_logging()
    test_save_shibor_rate()
    test_save_shibor_quote()
    test_save_shibor_ma()
    test_save_lpr()
    test_save_lpr_ma()
