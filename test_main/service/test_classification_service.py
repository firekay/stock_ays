# encoding: UTF-8
import main
from service import classfication_service as cservice


def test_save_industry_classified():
    cservice.save_industry_classified()


if __name__ == '__main__':
    main.setup_logging()
    test_save_industry_classified()

