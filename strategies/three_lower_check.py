# encoding: UTF-8

import sys
import getopt
import pandas as pd
from dal import transaction_dal as ts_dal
from service import base_service
from utils import util


def main(date, start_date=None, end_date=None):
    # stock = '300675'
    date = date if date else util.get_yesterday_line()
    start_date = start_date if start_date else '2011-09-01'
    end_date = end_date if end_date else '2017-09-18'

    print(
        'The date is: %s, the start_date is: %s, the end_date is: %s.' % (date, start_date, end_date)
    )
    print('check close price.')
    stock_codes = [stock.code for stock in base_service.get_stocks(date)]

    all_ascend_3 = 0
    all_descend_3 = 0
    all_ascend_4 = 0
    all_descend_4 = 0
    for stock in stock_codes:
        stocks = ts_dal.load_stock_k_data(model_ktype='D', stock=stock,
                                          start_date=start_date, end_date=end_date)
        # stocks = ts_dal.load_stock_k_data(model_ktype='D', stock=stock)
        # stocks = ts_dal.load_stock_k_data(model_ktype='D', start_date='2017-09-01', end_date='2017-09-18')
        stocks_df = pd.DataFrame(list(stocks.dicts()))
        if stocks_df.empty:
            print('No data for stock code %s' % stock)
            continue
        stocks_df = stocks_df[['close', 'open', 'high', 'low', 'volume']]
        stocks_df.close = stocks_df.close.astype(float)
        stocks_df.open = stocks_df.open.astype(float)
        stocks_df.high = stocks_df.high.astype(float)
        stocks_df.low = stocks_df.low.astype(float)
        stocks_df.volume = stocks_df.volume.astype(float)

        today_data = stocks_df[:-1].reset_index(drop=True)
        tomorrow_data = stocks_df[1:].reset_index(drop=True)
        sub_data = tomorrow_data - today_data
        count = 0
        ascend_3 = 0
        descend_3 = 0
        ascend_4 = 0
        descend_4 = 0

        for k, v in sub_data['close'].iteritems():
            if count >= 3:
                if v < 0:
                    descend_3 += 1
                    all_descend_3 += 1
                    count = 0
                else:
                    ascend_3 += 1
                    all_ascend_3 += 1
                    count = 0
            if v < 0:
                count += 1
            else:
                count = 0
        if descend_3 == 0 and ascend_3 == 0:
            print "code is: %s, No three continue ascend_3." % stock
        else:
            percent_3 = float(descend_3) / (ascend_3 + descend_3) * 100
            print "code is: %s, ascend_3 is %d, descend_3 is %d, percent_3 is %f" \
                  % (stock, ascend_3, descend_3, percent_3)
    if all_descend_3 == 0 and all_ascend_3 == 0:
        print "No three continue all_ascend_3."
    else:
        all_percent_3 = float(all_descend_3) / (all_ascend_3 + all_descend_3) * 100
        print "all_ascend_3 is %d, all_descend_3 is %d, all_percent_3 is %f" \
              % (all_ascend_3, all_descend_3, all_percent_3)

    # for stock in stock_codes:
    #     stocks = ts_dal.load_stock_k_data(model_ktype='D',
    #                                       stock=stock, start_date='2017-09-01', end_date='2017-09-18')
    #     # stocks = ts_dal.load_stock_k_data(model_ktype='D', start_date='2017-09-01', end_date='2017-09-18')
    #     stocks_df = pd.DataFrame(list(stocks.dicts()))
    #     stocks_df = stocks_df[['close', 'open', 'high', 'low', 'volume']]
    #     stocks_df.close = stocks_df.close.astype(float)
    #     stocks_df.open = stocks_df.open.astype(float)
    #     stocks_df.high = stocks_df.high.astype(float)
    #     stocks_df.low = stocks_df.low.astype(float)
    #     stocks_df.volume = stocks_df.volume.astype(float)
    #
    #     today_data = stocks_df[:-1].reset_index(drop=True)
    #     tomorrow_data = stocks_df[1:].reset_index(drop=True)
    #     sub_data = tomorrow_data - today_data
    #     count = 0
    #     ascend_3 = 0
    #     descend_3 = 0
    #     ascend_4 = 0
    #     descend_4 = 0
    #
    #     for k, v in sub_data['open'].iteritems():
    #         if v > 0:
    #             count += 1
    #         else:
    #             count = 0
    #         if count >= 3:
    #             if v > 0:
    #                 ascend_3 += 1
    #                 all_ascend_3 += 1
    #             else:
    #                 descend_3 += 1
    #                 all_descend_3 += 1
    #             if count >= 4:
    #                 if v > 0:
    #                     ascend_4 += 1
    #                     all_ascend_4 += 1
    #                 else:
    #                     descend_4 += 1
    #                     all_descend_4 += 1
    #
    #     percent_3 = 100
    #     if descend_3 != 0:
    #         percent_3 = float(ascend_3) / descend_3 * 100
    #     if descend_3 == 0 and ascend_3 == 0:
    #         print "code is: %s, No three continue ascend_3." % stock
    #     else:
    #         print "code is: %s, ascend_3 is %d, descend_3 is %d, percent_3 is %f" \
    #               % (stock, ascend_3, descend_3, percent_3)
    #
    #     percent_4 = 100
    #     if descend_4 != 0:
    #         percent_4 = float(ascend_4) / descend_4 * 100
    #     if descend_4 == 0 and ascend_4 == 0:
    #         print "code is: %s, No three continue ascend_4." % stock
    #     else:
    #         print "code is: %s, ascend_4 is %d, descend_4 is %d, percent_4 is %f" \
    #               % (stock, ascend_4, descend_4, percent_4)
    # all_percent_3 = 100
    # if all_descend_3 != 0:
    #     all_percent_3 = float(all_ascend_3) / all_descend_3 * 100
    # if all_descend_3 == 0 and all_ascend_3 == 0:
    #     print "No three continue all_ascend_3."
    # else:
    #     print "all_ascend_3 is %d, all_descend_3 is %d, all_percent_3 is %f" \
    #           % (all_ascend_3, all_descend_3, all_percent_3)
    #
    # all_percent_4 = 100
    # if all_descend_4 != 0:
    #     all_percent_4 = float(all_ascend_4) / all_descend_4 * 100
    # if all_descend_4 == 0 and all_ascend_4 == 0:
    #     print "No three continue all_ascend_4."
    # else:
    #     print "all_ascend_4 is %d, all_descend_4 is %d, all_percent_4 is %f" \
    #           % (all_ascend_4, all_descend_4, all_percent_4)

if __name__ == '__main__':
    try:
        options, args = getopt.getopt(sys.argv[1:], 'hd:s:e:', ['help', 'date=', 'start=', 'end='])
    except getopt.GetoptError:
        sys.exit()
    date = None
    start_date = None
    end_date = None
    for option, val in options:
        if option in ('-h', '--help'):
            print('Use -d or --date to assign the stock date(All this date\'s stocks.'
                  'Use -s or --start to assign the begin date.'
                  'use -e or --end to assign the end date.')
            sys.exit(1)
        if option in ('-d', '--date'):
            date = val
        if option in ('-s', '--start'):
            start_date = val
        if option in ('-e', '--end'):
            end_date = val
    main(date, start_date, end_date)
