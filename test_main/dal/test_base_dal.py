# encoding: UTF-8
import main
from dal import base_dal
from test_main.constants import *


def test_delete_performance_report():
    base_dal.delete_performance_report(YEAR, QUARTER)

if __name__ == '__main__':
    main.setup_logging()
    test_delete_performance_report()
