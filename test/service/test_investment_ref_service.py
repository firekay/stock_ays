# encoding: UTF-8
from service import investment_ref_service as irservice


def test_save_restricted_stock():
    irservice.save_restricted_stock(2017, 10)


if __name__ == '__main__':
    test_save_restricted_stock()
