# encoding: UTF-8
import main
from service import base_service
from test_main.constants import *


def test_save_performance_report():
    base_service.save_performance_report(YEAR, QUARTER)


if __name__ == '__main__':
    main.setup_logging()
    test_save_performance_report()
