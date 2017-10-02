# encoding: UTF-8
from service import investment_ref_service as irservice


def test_save_restricted_stock():
    irservice.save_restricted_stock(2017, 10)


def test_save_new_stocks():
    irservice.save_new_stocks()


    # test_save_restricted_stock()
    test_save_new_stocks()

