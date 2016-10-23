# encoding: UTF-8

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
import datetime


def get_today():
    return datetime.datetime.now().strftime('%Y%m%d')


def get_today_line():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_yestoday():
    return (datetime.datetime.now()+ datetime.timedelta(days = -1)).strftime('%Y%m%d')

def get_yestoday_line():
    return (datetime.datetime.now()+ datetime.timedelta(days = -1)).strftime('%Y-%m-%d')

def get_tomorrow():
    return (datetime.datetime.now()+ datetime.timedelta(days = 1)).strftime('%Y%m%d')

def get_tomorrow_line():
    return (datetime.datetime.now()+ datetime.timedelta(days = 1)).strftime('%Y-%m-%d')

def get_before_yestd_line():
    return (datetime.datetime.now()+ datetime.timedelta(days = -2)).strftime('%Y-%m-%d')


if __name__ == '__main__':
    print(get_today())
    print(str(get_today_line()))
    print(get_yestoday())
    print(str(get_yestoday_line()))
    print(str(get_before_yestd_line()))
    print(get_tomorrow())
    print(str(get_tomorrow_line()))
