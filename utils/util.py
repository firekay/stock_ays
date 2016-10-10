# encoding: UTF-8

from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import datetime

def get_today():
    return datetime.now().strftime('%Y%m%d')


if __name__ == '__main__':
    print(get_today())
    print(str(get_today()))
