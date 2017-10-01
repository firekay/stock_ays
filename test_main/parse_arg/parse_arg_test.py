# encoding: UTF-8

import argparse


def args_parse():
    parser = argparse.ArgumentParser(description='Get stock data with tushare')
    top_sub_parsers = parser.add_subparsers()

    # database table parser
    db_parser = top_sub_parsers.add_parser('d', help='database and table service')

    db_parser.add_argument('-d', action='store_true', dest='drop_table', help='drop all tables')
    db_parser.add_argument('-c', action='store_true', dest='create_table', help='create all tables')

    # transaction parser
    transaction_parser = top_sub_parsers.add_parser('t', help='transaction service')
    tran_sub_parsers = transaction_parser.add_subparsers()
    hist_parser = tran_sub_parsers.add_parser('h', help='hist data service')
    hist_parser.add_argument('-hi', action='store_true',
                                dest='save_stocks_hist_data',
                                help='save stocks history data')
    hist_parser.add_argument('-r', action='store_true',
                                    dest='save_stocks_revote_hist_data',
                                    help='save stocks revote history data')

    transaction_parser.add_argument('-t', action='store_true',
                                    dest='today_data',
                                    help='save today stocks history data, use with [--ktype]')
    transaction_parser.add_argument('-y', action='store_true',
                                    dest='yesterday_data',
                                    help='save yesterday stocks history data, use with [--ktype]')
    transaction_parser.add_argument('--start', dest='start_date', help='start date')
    transaction_parser.add_argument('--end', dest='end_date', help='end date')
    transaction_parser.add_argument('--ktype', dest='ktype',
                                    help='数据类型: D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟',
                                    choices=['D', 'W', 'M', '5', '15', '30', '60'])
    transaction_parser.add_argument('-a', action='store_true', dest='all_stocks', help='get all stocks data.')
    transaction_parser.add_argument('-s', action='store_true', dest='select_stocks', help='get select stocks data.')

    # fundamentals, basic parser
    fundamentals_parser = top_sub_parsers.add_parser('f', help='fundamentals service(include stock list)')
    fundamentals_parser.add_argument('-s', action='store_true', dest='save_stocks_basic_data',
                                        help='save stocks basic data')
    args = parser.parse_args()

    # print(args.drop_table)
    if hasattr(args, 'all_stocks'):
        if args.all_stocks:
            print('all_sotcks true')
        else:
            print('all_sotcks false')
    else:
        print('do not have all_sotcks attribute')
    # args = parser.parse_known_args()
    print(parser.print_help())
    # print(parser.print_usage())
    print(args)
    # db_parser.add_argument('-d', action='store_true', dest='drop_table', help='drop all tables')
    # db_parser.add_argument('-c', action='store_true', dest='create_table', help='create all tables')

    # # transaction parser
    # transaction_parser = top_sub_parsers.add_parser('t', help='transaction service')
    # tran_sub_parsers = transaction_parser.add_subparsers()
    # hist_parser = tran_sub_parsers.add_parser('h', help='hist and revote hist data service')
    # # hist_parser.add_argument('-h', action='store_true',
    # #                              dest='save_stocks_hist_data',
    # #                              help='save stocks history data, use with [--start] [--end] [-t] [-y] [-a] [-s] [--ktype] befor r parameter')
    # # hist_parser.add_argument('-a', action='store_true',
    # #                              dest='save_all_stocks_hist_data',
    # #                              help='save all stocks history data, use with [--start] [--end] [-t] [-y] [--ktype] befor r parameter')
    # # hist_parser.add_argument('-s', action='store_true',
    # #                              dest='save_select_stocks_hist_data',
    # #                              help='save select stocks history data, use with [--start] [--end] [-t] [-y] [--ktype] befor r parameter')
    # hist_revote_parser = tran_sub_parsers.add_parser('r', help='hist revote data service')
    # hist_revote_parser.add_argument('-a', action='store_true',
    #                              dest='save_all_stocks_revote_hist_data',
    #                              help='save all  stocks revote history data, use with [--start] [--end] [-t] [-y] [--ktype] befor r parameter')
    # hist_revote_parser.add_argument('-s', action='store_true',
    #                              dest='save_select_stocks_revote_hist_data',
    #                                 help='save select stocks revote history data, use with [--start] [--end] [-t] [-y] [--ktype] befor r parameter')

    # transaction_parser.add_argument('-t', action='store_true',
    #                              dest='today_data',
    #                              help='save today stocks history data, use with [--ktype]')
    # transaction_parser.add_argument('-y', action='store_true',
    #                              dest='yesterday_data',
    #                              help='save yesterday stocks history data, use with [--ktype]')
    # transaction_parser.add_argument('--start', dest='start_date', help='start date')
    # transaction_parser.add_argument('--end', dest='end_date', help='end date')
    # transaction_parser.add_argument('--ktype', dest='ktype', help='数据类型: D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟',
    #                             choices=['D', 'W', 'M', '5', '15', '30', '60'])
    # transaction_parser.add_argument('-a', action='store_true', dest='all_stocks', help='get all stocks data.')
    # transaction_parser.add_argument('-s', action='store_true', dest='select_stocks', help='get select stocks data.')

    # # fundamentals, basic parser
    # fundamentals_parser = top_sub_parsers.add_parser('f', help='fundamentals service(include stock list)')
    # fundamentals_parser.add_argument('-s', action='store_true', dest='save_stocks_basic_data',
    #                               help='save stocks basic data')

    # args = parser.parse_args()
    # # print(args.drop_table)
    # if hasattr(args, 'all_stocks'):
    #     if args.all_stocks:
    #         print('all_sotcks true')
    #     else:
    #         print('all_sotcks false')
    # else:
    #     print('do not have all_sotcks attribute')
    # # args = parser.parse_known_args()
    # # print(parser.print_help())
    # # print(parser.print_usage())
    # print(args)





    # subparsers = parser.add_subparsers(help='subparsers')
    # table_parser = subparsers.add_parser('tb', help='for table service')
    # tp_subpsarsers = table_parser.add_subparsers(help='table service subparser')
    # tp_sub_parser = tp_subpsarsers.add_parser('sub_tp', help='tb subparser test')
    # tp_sub_parser.add_argument('-stpd', action='store_true', dest='drop_table', help='drop all tables')
    # tp_sub_parser.add_argument('-stpc', action='store_true', dest='create_table', help='create all tables')
    # table_parser.add_argument('-d', action='store_true', dest='drop_table', help='drop all tables')
    # table_parser.add_argument('-c', action='store_true', dest='create_table', help='create all tables')
    # transaction = subparsers.add_parser('tt', help='for transaction service')
    # transaction.add_argument('-t-a-a-h-d', action='store_true', dest='save_all_days_all_stocks_hist_data', help='save all days all stocks history data')
    # transaction.add_argument('-t-a-s-h-d', action='store_true', dest='save_all_days_select_stocks_hist_data', help='save all days selected all stocks history data')




    # tt_parser = argparse.ArgumentParser(description='transaction')
    # transaction = parser.add_argument_group('transaction')
    # transaction.add_argument('-t-a-a-h-d', action='store_true', dest='save_all_days_all_stocks_hist_data', help='save all days all stocks history data')
    # transaction.add_argument('-t-a-s-h-d', action='store_true', dest='save_all_days_select_stocks_hist_data', help='save all days selected all stocks history data')

    # transaction.add_argument('-t-t-a-h-d', action='store_true', dest='save_today_all_stocks_hist_data', help='save today all stocks history data')
    # transaction.add_argument('-t-t-s-h-d', action='store_true', dest='save_today_select_stocks_hist_data', help='save today selected stocks history data')

    # transaction.add_argument('-t-y-a-h-d', action='store_true', dest='save_yestoday_all_stocks_hist_data', help='save yestoday all stocks history data')
    # transaction.add_argument('-t-y-s-h-d', action='store_true', dest='save_yestoday_select_stocks_hist_data', help='save yestoday selected stocks history data')
    # transaction.add_argument('--ktype', dest='ktype', help='数据类型: D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟',
    #                              choices=['D', 'W', 'M', '5', '15', '30', '60'])


    # subparsers = parser.add_subparsers()
    # transaction_selected = subparsers.add_parser('-t-a-s-h-d', help='save all selected stocks history data')
    # transaction_selected.add_argument('--stocks', nargs='+', dest='stocks_selected', help='save all selected stocks history data')
    # transaction_selected.add_argument('-ktype', choices=['D', 'W', 'M'], help='save the sotck type, D is day, W is week, M is month')
    


    # args = parser.parse_known_args()


def main():
    args_parse()


if __name__ == '__main__':
    main()
