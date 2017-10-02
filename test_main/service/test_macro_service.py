# encoding: UTF-8
import test_main
from service import macro_service


def test_save_deposit_rate():
    macro_service.save_deposit_rate()


def test_save_loan_rate():
    macro_service.save_loan_rate()

if __name__ == '__main__':
    test_main.setup_logging()
    # test_save_loan_rate()
    test_save_deposit_rate()
