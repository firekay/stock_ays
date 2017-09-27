# encoding: UTF-8
""""""

import logging
from utils.mysql_utils import *
from models.model import *
from service import table_service
from service import data_service

logger = logging.getLogger(__name__)


# @conn
def save_stocks_basic_data():
    table_service.truncate_table(StockBasic)
    data_service.save_stock_basic()
