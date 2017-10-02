# encoding: utf-8
import logging
from dal import investment_ref_dal as irdal
from utils import util


logger = logging.getLogger(__name__)


def save_distribution_plans(year, top=5000):
    """存储分配预案数据"""
    data_dicts = irdal.get_distribution_plans_data(year, top)
    if data_dicts:
        irdal.save_distribution_plans_data(data_dicts)


def save_restricted_stock(year=None, month=None):
    year = util.get_year() if year is None else year
    month = util.get_month() if month is None else month
    """存储限售股解禁"""
    data_dicts = irdal.get_restricted_stock(year, month)
    if data_dicts:
        if irdal.delete_restricted_stock(year, month):
            irdal.save_restricted_stock(data_dicts, year, month)


def save_performance_forecast(year, quarter):
    data_dicts = irdal.get_performance_forecast(year, quarter)
    if data_dicts:
        if irdal.delete_performance_forecast(year, quarter):
            irdal.save_performance_forecast(data_dicts, year, quarter)


def save_new_stocks():
    new_stocks_dal = irdal.NewStocksDal()
    data_dicts = new_stocks_dal.get_new_stocks()
    if data_dicts:
        new_stocks_dal.save_new_stocks(data_dicts)


def save_financing_securities_sh(start_date=None, end_date=None):
    fs_sh_dal = irdal.FinancingSecuritiesShDal()
    data_dicts = fs_sh_dal.get_financing_securities_sh(start_date, end_date)
    if data_dicts:
        fs_sh_dal.save_financing_securities_sh(data_dicts)


def save_financing_securities_detail_sh(start_date, end_date=None):
    # 如果end_date为None, 则只有start_date一天的的数据
    fsd_sh_dal = irdal.FinancingSecuritiesDetailShDal()
    if end_date:
        data_dicts = fsd_sh_dal.get_financing_securities_detail_sh(start_date=start_date, end_date=end_date)
        if data_dicts:
            if fsd_sh_dal.delete_some_days_data(start_date=start_date, end_date=end_date):
                fsd_sh_dal.save_financing_securities_detail_sh(data_dicts,
                                                               start_date=start_date,end_date=end_date)
    else:
        data_dicts = fsd_sh_dal.get_financing_securities_detail_sh(date=start_date)
        if data_dicts:
            if fsd_sh_dal.delete_some_days_data(date=start_date):
                fsd_sh_dal.save_financing_securities_detail_sh(data_dicts, date=start_date)
