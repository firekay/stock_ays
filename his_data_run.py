# encoding: UTF-8
import logging
import logging.config
from service import business_service as bser

logging.config.fileConfig("logging.conf")
logger = logging.getLogger()

def save_data():
    """下载并保持交易数据"""

    logger.info('Begin save today all stocks history data')
    # bser.save_yestoday_all_stocks_his_data()
    bser.save_today_all_stocks_his_data()
    logger.info('End save today all stocks history data')

def main():
    save_data()


if __name__ == '__main__':
    main()
