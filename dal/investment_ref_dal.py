# encoding: UTF-8

import logging
import tushare as ts

from dal.constants import *
from models.model import *
from utils import util
from dal import util_dal

logger = logging.getLogger(__name__)


today_line = util.get_today_line()


def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989:
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True


def get_distribution_plans_data(year, top=25, retry_count=RETRY_COUNT, pause=PAUSE):
    """得到分配预案数据
    
    Args:
        year : 预案公布的年份，默认为2014
        top :取最新n条数据，默认取最近公布的25条
        retry_count：当网络异常后重试次数，默认为3
        pause:重试时停顿秒数，默认为0
    Returns:
        data_dicts: 字典的列表, 具体的字段及值, 如果没有返回空列表, 如果接口出错返回None
    """
    logger.info('Begin get distribution plans, the year is %s' % year)
    try:
        data_df = ts.profit_data(year=year, top=top, retry_count=retry_count, pause=pause)
    except Exception as e:
        logger.exception('Error get distribution plans, the year is %s' % year)
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get distribution plans, the year is %s' % year)
        else:
            data_dicts = [{'year': year, 'code': row[0], 'name': row[1], 'report_date': row[3],
                          'divi': row[4], 'shares': row[5], 'insert_date': today_line}
                         for row in data_df.values]
            logger.info('Success get distribution plans, the year is %s' % year)
        return data_dicts


def save_distribution_plans_data(data_dicts, year):
    """存储分配预案数据
    
    Args:
        data_dicts: 字典的列表, 具体的字段及值
        year: 年份, YYYY格式
        """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save distribution plans, the year is %s' % year)
    try:
        DistributionPlans.insert_many(data_dicts).execute()
        logger.info('Success save distribution plans, the year is %s' % year)
    except Exception as e:
        logger.exception('Error save distribution plans, the year is %s' % year)


def get_performance_forecast(year, quarter):
    """得到业绩预告
    
    Args:
        year: 年份, YYYY格式数字
        quarter: 季度, 只能是1, 2, 3, 4的数字
    Returns:
        data_dicts: 字段的列表, return None if have exception, return empty if no data
        """
    _check_input(year, quarter)
    logger.info('Begin get performance forecast data, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.forecast_data(year=year, quarter=quarter)
    except Exception as e:
        logging.exception('Error get performance forecast data, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get performance forecast data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'type': row[2], 'report_date': row[3], 'pre_eps': row[4],
                           'range': row[5], 'insert_date': today_line} for row in data_df.values]
            logger.info('Success get performance forecast data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


def get_restricted_stock(year=None, month=None, retry_count=RETRY_COUNT, pause=PAUSE):
    """
    获取限售股解禁数据
    Args
        year:年份,默认为当前年
        month:解禁月份，默认为当前月
        retry_count : int, 默认 3
                     如遇网络等问题重复执行的次数 
        pause : int, 默认 0
    Returns:
        字典的列表
    """
    year = util.get_year() if year is None else year
    month = util.get_month() if month is None else month
    logger.info('Begin get restricted stock data, the year is: %s, month is: %s'
                % (year, month))
    try:
        data_df = ts.xsg_data(year=year, month=month, retry_count=retry_count, pause=pause)
    except Exception as e:
        logging.exception('Error get restricted stock data, the year is: %s, month is: %s'
                % (year, month))
        return None
    else:
        data_dicts = []
        if not data_df.empty:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'month': month,
                           'date': row[2], 'count': row[3], 'ratio': row[4], 'insert_date': today_line}
                          for row in data_df.values]
            logger.info('Success get restricted stock data, the year is: %s, month is: %s'
                        % (year, month))
        else:
            logger.warn('Empty get restricted stock data, the year is: %s, month is: %s'
                        % (year, month))
        return data_dicts


def save_restricted_stock(data_dicts, year, month):
    """保存限售股解禁数据"""
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save restricted stock data, the year is: %s, month is: %s'
                % (year, month))
    try:
        RestrictedStock.insert_many(data_dicts).execute()
        logger.info('Success save restricted stock data, the year is: %s, month is: %s'
                    % (year, month))
        return True
    except Exception as e:
        logger.exception('Error save restricted stock data, the year is: %s, month is: %s'
                         % (year, month))
        return False


def get_fund_holdings(year, quarter, retry_count=RETRY_COUNT, pause=PAUSE):
    _check_input(year, quarter)
    logger.info('Begin get fund holdings data, the year is: %s, quarter is: %s'
                % (year, quarter))
    try:
        data_df = ts.fund_holdings(year=year, quarter=quarter, retry_count=retry_count, pause=pause)
    except Exception:
        logging.exception('Error get fund holdings data, the year is: %s, quarter is: %s'
                          % (year, quarter))
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get fund holdings data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        else:
            data_dicts = [{'code': row[0], 'name': row[1], 'year': year, 'quarter': quarter,
                           'date': row[2], 'nums': row[3], 'nlast': row[4], 'count': row[5],
                           'clast': row[6], 'amount': row[7], 'ratio': row[8],
                           'insert_date': today_line} for row in data_df.values]
            logger.info('Success get fund holdings data, the year is: %s, quarter is: %s'
                        % (year, quarter))
        return data_dicts


class NewStocksDal(object):

    def get_new_stocks(self, retry_count=RETRY_COUNT, pause=PAUSE):
        logger.info('Begin get new stocks.')
        try:
            data_df = ts.new_stocks(retry_count, pause)
        except Exception:
            logger.exception('Error get new stocks.')
            return None
        else:
            data_dicts = []
            if data_df.empty:
                logger.warn('Empty get get new stocks.')
            else:
                data_dicts = [{'code': row[0], 'xcode': row[1], 'name': row[2], 'ipo_date': row[3],
                               'issue_date': row[4], 'amount': row[5], 'markets': row[6], 'price': row[7],
                               'pe': row[8], 'limit': row[9], 'funds': row[10], 'ballot': row[11],
                               'insert_date': today_line} for row in data_df.values]
                logger.info('Success get get new stocks.')
            return data_dicts

    def delete_new_stocks(self):
        pass

    def select_new_stock(self, code):
        pass

    def select_new_stock_all_codes(self):
        stocks = NewStocks.select(NewStocks.code)
        return [stock.code for stock in stocks]

    def save_new_stocks(self, data_dicts):
        assert data_dicts, 'data_dict must not empty and data_dict must not None'
        save_ok = True
        logger.info('Begin save all new stocks.')
        new_codes = self.select_new_stock_all_codes()
        for row in data_dicts:
            code = row.get('code')
            if code not in new_codes:
                try:
                    NewStocks.insert(row).execute()
                except Exception:
                    logger.exception('Error save new stock, the stock code is %s.' % code)
                    save_ok = False
        if save_ok:
            logger.info('Success save all new stocks.')
        else:
            logger.error('End but not success save all new stocks.')
        return save_ok


class FinancingSecuritiesShDal(object):

    def select_financing_securities_sh_all_days(self):
        fs_shs = FinancingSecuritiesSh.select(FinancingSecuritiesSh.op_date)
        return [util.date2str(fs_sh.op_date) for fs_sh in fs_shs]

    def get_financing_securities_sh(self, start_date=None, end_date=None,
                                    retry_count=RETRY_COUNT, pause=PAUSE):
        logger.info('Begin get financing securities sh data, start_date is %s,'
                    ' end_date is %s.' % (start_date, end_date))
        data_dicts = []
        try:
            data_df = ts.sh_margins(start=start_date, end=end_date,
                                    retry_count=retry_count, pause=pause)
        except Exception:
            logger.exception('Error get financing securities sh data, start_date is %s, '
                             'end_date is %s.' % (start_date, end_date))
        else:
            if data_df.empty:
                logger.warn('Empty get financing securities sh data, start_date is %s,'
                            ' end_date is %s.' % (start_date, end_date))
            else:
                data_dicts = [{'op_date': row[0], 'rzye': row[1], 'rzmre': row[2], 'rqyl': row[3],
                               'rqylje': row[4], 'rqmcl': row[5], 'rzrqjyzl': row[6]}
                               for row in data_df.values]
                logger.info('Success get financing securities sh data, start_date is %s,'
                            ' end_date is %s.' % (start_date, end_date))
        return data_dicts

    def save_financing_securities_sh(self, data_dicts):
        assert data_dicts, 'data_dict must not empty and data_dict must not None'
        save_ok = True
        logger.info('Begin save financing securities sh data.')
        dates = self.select_financing_securities_sh_all_days()
        for row in data_dicts:
            dt = row.get('op_date')
            if dt not in dates:
                try:
                    FinancingSecuritiesSh.insert(row).execute()
                except Exception:
                    logger.exception('Error save financing securities sh data.')
                    save_ok = False
        if save_ok:
            logger.info('Success save all financing securities sh data.')
        else:
            logger.error('End but not success save all financing securities sh data.')
        return save_ok


class FinancingSecuritiesDetailShDal(object):

    def delete_some_days_data(self, date=None, start_date=None, end_date=None):
        # date must be not None, or start_date and end_date must not None.
        delete_ok = True
        if date is not None:
            logger.info('Begin delete financing securities details sh data. Date is %s' % date)
            try:
                FinancingSecuritiesDetailSh.delete()\
                    .where(FinancingSecuritiesDetailSh.op_date == date).execute()
                logger.info('Success delete financing securities details sh data. Date is %s'
                            % date)
            except Exception:
                delete_ok = False
                logger.exception('Error delete financing securities details sh data. Date is %s'
                                 % date)
        elif start_date is not None and end_date is not None:
            logger.info('Begin delete financing securities details sh data. Start_date is %s,'
                        ' end_date is %s' % (start_date, end_date))
            try:
                FinancingSecuritiesDetailSh.delete()\
                    .where(FinancingSecuritiesDetailSh.op_date >= start_date,
                           FinancingSecuritiesDetailSh.op_date <= end_date).execute()
                logger.info('Success delete financing securities details sh data. Start_date is %s,'
                            ' end_date is %s' % (start_date, end_date))
            except Exception:
                delete_ok = False
                logger.exception('Error delete financing securities details sh data. Start_date is %s,'
                                 ' end_date is %s' % (start_date, end_date))
        else:
            raise TypeError('date must be not None, or start_date and end_date must not None.')
        return delete_ok

    def get_financing_securities_detail_sh(self, date=None, start_date=None, end_date=None,
                                           retry_count=RETRY_COUNT, pause = PAUSE):
        # 1. 参数全为空; 2. 只有date 3. 只有start_date和end_date
        # logger.info('Begin get financing securities details sh data. Date is %s,'
        #             ' start_date is %s, end_date is %s' % (date, start_date, end_date))
        if date is not None:
            logger.info('Begin get financing securities details sh data. Date is %s' % date)
            try:
                data_df = ts.sh_margin_details(date=date, retry_count=retry_count, pause=pause)
            except Exception:
                logger.exception('Begin get financing securities details sh data. Date is %s' % date)
                return None
        elif start_date is not None and end_date is not None:
            logger.info('Begin get financing securities details sh data.'
                        ' Start_date is %s, end_date is %s.' % (start_date, end_date))
            try:
                data_df = ts.sh_margin_details(start=start_date, end=end_date,
                                               retry_count=retry_count, pause=pause)
            except Exception:
                logger.exception('Error get financing securities details sh data.'
                                 ' Start_date is %s, end_date is %s.' % (start_date, end_date))
                return None
        elif not date and not start_date and not end_date:
            logger.info('Begin get financing securities details sh data.')
            try:
                data_df = ts.sh_margin_details(date='', start='', end='',
                                               retry_count=retry_count, pause=pause)
            except Exception:
                logger.exception('Begin get financing securities details sh data.')
                return None
        else:
            raise TypeError('1. 参数全为空; 2. 只有date 3. 只有start_date和end_date')
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get financing securities details sh data. date is: %s, '
                        'start_date is %s, end_date is: %s' % (date, start_date, end_date))
        else:
            data_dicts = [{'op_date': row[0], 'stock_code': row[1], 'security_abbr': row[2], 'rzye': row[3],
                           'rzmre': row[4], 'rzche': row[5], 'rqyl': row[6], 'rqmcl': row[7],
                           'rqchl': row[8]} for row in data_df.values]
            logger.info('Success get financing securities details sh data. date is %s,'
                        'start_date is %s, end_date is: %s' % (date, start_date, end_date))
        return data_dicts

    def save_financing_securities_detail_sh(self, data_dicts, date=None, start_date=None, end_date=None):
        save_ok = True
        assert data_dicts, 'data_dict must not empty and data_dict must not None'
        assert date or (start_date and end_date), 'date not None, or start_date and end_date not None.'
        if date:
            logger.info('Begin save financing security details sh, date is %s' % date)
        else:
            logger.info('Begin save financing security details sh, start_date is %s,'
                        ' end_date is %s.' % (start_date, end_date))
        try:
            FinancingSecuritiesDetailSh.insert_many(data_dicts).execute()
            if date:
                logger.info('Success save financing security details sh, date is %s' % date)
            else:
                logger.info('Success save financing security details sh, start_date is %s,'
                            ' end_date is %s.' % (start_date, end_date))
        except Exception:
            save_ok = False
            if date:
                logger.exception('Error save financing security details sh, date is %s' % date)
            else:
                logger.exception('Error save financing security details sh, start_date is %s,'
                                 ' end_date is %s.' % (start_date, end_date))
        return save_ok


class FinancingSecuritiesSzDal(object):

    def select_financing_securities_sz_all_days(self):
        fs_szs = FinancingSecuritiesSz.select(FinancingSecuritiesSz.op_date)
        return [util.date2str(fs_sz.op_date) for fs_sz in fs_szs]

    def get_financing_securities_sz(self, start_date=None, end_date=None,
                                    retry_count=RETRY_COUNT, pause=PAUSE):
        logger.info('Begin get financing securities sz data, start_date is %s,'
                    ' end_date is %s.' % (start_date, end_date))
        data_dicts = []
        try:
            data_df = ts.sz_margins(start=start_date, end=end_date,
                                    retry_count=retry_count, pause=pause)
        except Exception:
            logger.exception('Error get financing securities sz data, start_date is %s,'
                             ' end_date is %s.' % (start_date, end_date))
        else:
            if data_df.empty:
                logger.warn('Empty get financing securities sz data, start_date is %s,'
                            ' end_date is %s.' % (start_date, end_date))
            else:
                data_dicts = [{'rzmre': row[0], 'rzye': row[1], 'rqmcl': row[2], 'rqyl': row[3],
                               'rqye': row[4], 'rzrqye': row[5], 'op_date': row[6]}
                               for row in data_df.values]
                logger.info('Success get financing securities sz data, start_date is %s,'
                            ' end_date is %s.' % (start_date, end_date))
        return data_dicts

    def save_financing_securities_sz(self, data_dicts):
        assert data_dicts, 'data_dict must not empty and data_dict must not None'
        save_ok = True
        logger.info('Begin save financing securities sz data.')
        dates = self.select_financing_securities_sz_all_days()
        for row in data_dicts:
            dt = row.get('op_date')
            if dt not in dates:
                try:
                    FinancingSecuritiesSz.insert(row).execute()
                except Exception:
                    logger.exception('Error save financing securities sz data.')
                    save_ok = False
        if save_ok:
            logger.info('Success save all financing securities sz data.')
        else:
            logger.error('End but not success save all financing securities sz data.')
        return save_ok

    
class FinancingSecuritiesDetailSzDal(object):

    def delete_some_day_data(self, date):
        # date must be not None
        assert date is not None, 'date must be not None or \'\''
        delete_ok = True
        logger.info('Begin delete financing securities details sz data. Date is %s' % date)
        try:
            FinancingSecuritiesDetailSz.delete()\
                .where(FinancingSecuritiesDetailSz.op_date == date).execute()
            logger.info('Success delete financing securities details sz data. Date is %s' % date)
        except Exception:
            delete_ok = False
            logger.exception('Error delete financing securities details sz data. Date is %s' % date)
        return delete_ok

    def get_financing_securities_detail_sz(self, date,
                                           retry_count=RETRY_COUNT, pause=PAUSE):
        assert date is not None, 'date must be not None or \'\''
        logger.info('Begin get financing securities details sz data. Date is %s.' % date)
        try:
            data_df = ts.sz_margin_details(date=date, retry_count=retry_count, pause=pause)
        except Exception:
            logger.exception('Begin get financing securities details sz data. Date is %s' % date)
        data_dicts = []
        if data_df is None or data_df.empty:
            logger.warn('Empty get financing securities details sz data date, date is %s.' % date)
        else:
            data_dicts = [{'stock_code': row[0], 'security_abbr': row[1], 'rzmre': row[2], 'rzye': row[3],
                           'rqmcl': row[4], 'rqyl': row[5], 'rqye': row[6], 'rzrqye': row[7],
                           'op_date': row[8]} for row in data_df.values]
            logger.info('Success get financing securities details sz data, date is: %s.' % date)
        return data_dicts

    def save_financing_securities_detail_sz(self, data_dicts, date=None):
        return util_dal.save_date_data(FinancingSecuritiesDetailSz, data_dicts, date)
