# encoding: UTF-8

import datetime
import time
import tushare as ts

delta1 = datetime.timedelta(days=1)


def str2date(date):
    """
    Args:
        date: String type like: '2017-01-01'
    Returns:

    """
    return datetime.datetime.strptime(date, '%Y-%m-%d')


def date2str(date_s):
    return date_s.strftime('%Y-%m-%d')


def range_date_all_include(start_str, end_str):
    """得到给定日期内的开盘日期"""
    dates = ts.trade_cal()
    filter_dates = dates[(dates.calendarDate >= start_str) & (dates.calendarDate <= end_str)]
    open_dates = filter_dates.query('isOpen==1')
    for _, date in open_dates['calendarDate'].iteritems():
        yield date


def range_date_exclude_end(start_str, end_str):
    """循环给定的时间字符串(包含开头, 不包含结尾)"""
    start_d = str2date(start_str)
    end_d = str2date(end_str)
    while start_d < end_d:
        yield date2str(start_d)
        start_d += delta1


def get_now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def int2time(timestamp):
    datearr = datetime.datetime.utcfromtimestamp(timestamp)
    timestr = datearr.strftime("%Y-%m-%d %H:%M:%S")
    return timestr


def diff_day(start=None, end=None):
    d1 = datetime.datetime.strptime(end, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(start, '%Y-%m-%d')
    delta = d1 - d2
    return delta.days


def get_year():
    year = datetime.datetime.today().year
    return year


def get_month():
    month = datetime.datetime.today().month
    return month


def get_hour():
    return datetime.datetime.today().hour


def get_today():
    return datetime.datetime.now().strftime('%Y%m%d')


def get_time():
    return datetime.datetime.now()


def get_today_line():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def get_yesterday():
    return (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y%m%d')


def get_yesterday_line():
    return (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')


def get_tomorrow():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')


def get_tomorrow_line():
    return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')


def get_ndays_before_line(n):
    return (datetime.datetime.now() + datetime.timedelta(days=-n)).strftime('%Y-%m-%d')


if __name__ == '__main__':
    start = '2017-09-04'
    end = '2017-09-27'
    for date in range_date_all_include(start, end):
        print(date)

        # print(get_today())
    # print(str(get_today_line()))
    # print(get_yesterday())
    # print(str(get_yesterday_line()))
    # print(get_tomorrow())
    # print(str(get_tomorrow_line()))
    # print(get_ndays_before_line(6))
