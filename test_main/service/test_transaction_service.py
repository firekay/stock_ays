# encoding: UTF-8
import test_main
from service import transaction_service as tservice

stocks = ['000001', '000002']


def test_save_stock_k_data(ktype, stocks=None):
    tservice.save_stocks_k_data()
    # tservice.save_stocks_k_data(ktype=ktype, stocks=stocks, start_date='2017-09-06', end_date='2017-09-12')


def test_save_yesterday_stocks_k_data(stocks=None, ktype=None):
    tservice.save_yesterday_stocks_k_data(stocks=stocks, ktype=ktype)


def test_save_today_stocks_k_data(stocks=None, ktype=None):
    tservice.save_today_stocks_k_data(stocks=stocks, ktype=ktype)


def test_save_stocks_hist_data(ktype, stocks=None):
    # tservice.save_stocks_hist_data(stocks=stocks, ktype=ktype, start_date='2017-09-06', end_date='2017-09-09')
    # tservice.save_stocks_hist_data(stocks=stocks, ktype=ktype)
    tservice.save_stocks_hist_data()


def test_save_yesterday_stocks_hist_data(stocks=None, ktype=None):
    tservice.save_yesterday_stocks_hist_data(stocks=stocks, ktype=ktype)


def test_save_today_stocks_hist_data(stocks=None, ktype=None):
    tservice.save_today_stocks_hist_data(stocks=stocks, ktype=ktype)


def test_save_stock_h_data_revote(stocks=None):
    tservice.save_stock_h_data_revote(stocks, start_date='2017-09-06', end_date='2017-09-09')
    # tservice.save_stock_h_data_revote(stocks)


def test_save_today_all_data():
    tservice.save_today_all_data()


def test_save_tick_data(stocks=None):
    tservice.save_tick_data(stocks=stocks, date='2017-09-21')


def test_save_range_tick_data(stocks=None):
    tservice.save_tick_data_range(stocks=stocks, start_date='2017-09-19', end_date='2017-09-21')


def test_save_today_tick_data(stocks=None):
    tservice.save_today_tick_data(stocks=stocks)


def test_save_big_index_data():
    tservice.save_big_index_data()


def test_save_big_trade_data(stocks=None):
    tservice.save_big_trade_data(stocks=stocks, date='2017-9-13')


def test_save_big_trade_data_range(stocks=None):
    tservice.save_big_trade_data_range(stocks=stocks, start_date='2017-9-13', end_date='2017-9-16',)

if __name__ == '__main__':
    test_main.setup_logging()
    ktype='30'
    # test_save_stock_k_data(ktype, stocks)
    # test_save_today_stocks_k_data(stocks=stocks, ktype=ktype)
    # test_save_yesterday_stocks_k_data(stocks=stocks, ktype=ktype)
    test_save_stocks_hist_data(ktype=ktype, stocks=stocks)
    # test_save_today_stocks_hist_data(stocks=stocks, ktype=ktype)
    # test_save_yesterday_stocks_hist_data(stocks=stocks, ktype=ktype)
    # test_save_stock_h_data_revote(stocks)
    # test_save_today_all_data()
    # test_save_tick_data(stocks)
    # test_save_today_tick_data(stocks)
    # test_save_range_tick_data(stocks)
    # test_save_big_index_data()
    # test_save_big_trade_data(stocks)
    # test_save_big_trade_data_range(stocks)



