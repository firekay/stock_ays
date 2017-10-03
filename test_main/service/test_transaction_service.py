# encoding: UTF-8
import test_main
from service import transaction_service as tservice


def test_save_stock_k_data():
    tservice.save_stocks_k_data(ktype='D')

if __name__ == '__main__':
    test_main.setup_logging()

    test_save_stock_k_data()
