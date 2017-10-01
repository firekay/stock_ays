# encoding: UTF-8
import main
from service import investment_ref_service as irservice


def test_save_restricted_stock():
    irservice.save_restricted_stock(2017, 10)


def test_save_new_stocks():
    irservice.save_new_stocks()

if __name__ == '__main__':
    main.setup_logging()

    # test_save_restricted_stock()
    test_save_new_stocks()

