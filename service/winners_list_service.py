# encoding: UTF-8
""""""

import logging
from models.model import *
from dal import winners_list_dal as wllist_dal
from dal import util_dal


today_line = get_today_line()

DAYS_TYPE = [5, 10, 30, 60]


def save_top_list(date):
    """每日龙虎榜列表"""
    data_dicts = wllist_dal.get_top_list(date)
    if data_dicts:
        if util_dal.delete_date_data(TopList, date):
            util_dal.save_date_data(TopList, data_dicts, date)


def save_individual_statistics_tops(days_type=None):
    """个股上榜统计"""
    def _save_individual_statistics_tops(day_type):
        data_dicts = wllist_dal.get_individual_statistics_tops(day_type)
        if data_dicts:
            if util_dal.delete_insert_date_days_type_data(IndividualStatisticsTops, today_line, day_type):
                util_dal.save_date_day_type_data(IndividualStatisticsTops, data_dicts, today_line, day_type)
    if not days_type:
        for d in DAYS_TYPE:
            _save_individual_statistics_tops(d)
    elif isinstance(days_type, list):
        for d in days_type:
            _save_individual_statistics_tops(d)
    else:
        _save_individual_statistics_tops(days_type)


def save_broker_tops(days_type=None):
    """营业部上榜统计"""
    def _save_broker_tops(day_type):
        data_dicts = wllist_dal.get_broker_tops(day_type)
        if data_dicts:
            if util_dal.delete_insert_date_days_type_data(BrokerTops, today_line, day_type):
                util_dal.save_date_day_type_data(BrokerTops, data_dicts, today_line,day_type)
    if not days_type:
        for d in DAYS_TYPE:
            _save_broker_tops(d)
    elif isinstance(days_type, list):
        for d in days_type:
            _save_broker_tops(d)
    else:
        _save_broker_tops(days_type)


def save_institution_tops(days_type=None):
    """机构席位追踪"""
    def _save_institution_tops(day_type):
        data_dicts = wllist_dal.get_institution_tops(day_type)
        if data_dicts:
            if util_dal.delete_insert_date_days_type_data(InstitutionTops, today_line, day_type):
                util_dal.save_date_day_type_data(InstitutionTops, data_dicts, today_line, day_type)
    if not days_type:
        for d in DAYS_TYPE:
            _save_institution_tops(d)
    elif isinstance(days_type, list):
        for d in days_type:
            _save_institution_tops(d)
    else:
        _save_institution_tops(days_type)


def save_institution_detail():
    """机构成交明细"""
    data_dicts = wllist_dal.get_institution_detail()
    if data_dicts:
        if util_dal.delete_insert_date_data(InstitutionDetail, today_line):
            util_dal.save_date_data(InstitutionDetail, data_dicts, today_line)
