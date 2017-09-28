# encoding: UTF-8

import datetime

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


def range_date(start_str, end_str):
    """循环给定的时间字符串(包含开头, 不包含结尾)"""
    start_d = str2date(start_str)
    end_d = str2date(end_str)
    while start_d < end_d:
        yield date2str(start_d)
        start_d += delta1


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
    start = '2016-01-01'
    end = '2016-02-02'
    for date in range_date(start, end):
        print(date)

        # print(get_today())
    # print(str(get_today_line()))
    # print(get_yesterday())
    # print(str(get_yesterday_line()))
    # print(get_tomorrow())
    # print(str(get_tomorrow_line()))
    # print(get_ndays_before_line(6))
