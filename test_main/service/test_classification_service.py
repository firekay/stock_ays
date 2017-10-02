# encoding: UTF-8
import test_main
from service import classfication_service as cservice


def test_save_industry_classified():
    cservice.save_industry_classified()


if __name__ == '__main__':
    test_main.setup_logging()
    test_save_industry_classified()

