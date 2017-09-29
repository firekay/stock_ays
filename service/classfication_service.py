# encoding: UTF-8

import logging
from dal import classification_dal
from service import table_service
from models.model import *


logger = logging.getLogger(__name__)


def save_industry_classified():
    """处理行业分类"""
    logger.info('save_industry_classified')
    table_service.truncate_table(IndustryClassified)
    classification_dal.save_industry_classified()


def save_concept_classified():
    """处理股票概念分类.现实的二级市场交易中，经常会以”概念”来炒作，在数据分析过程中，可根据概念分类监测资金等信息的变动情况。"""
    table_service.truncate_table(ConceptClassified)
    classification_dal.save_concept_classified()


def save_area_classified():
    """按地域对股票进行分类，即查找出哪些股票属于哪个省份。"""
    table_service.truncate_table(AreaClassified)
    classification_dal.save_area_classified()

    
def save_sme_classified():
    """获取中小板股票数据，即查找所有002开头的股票"""
    table_service.truncate_table(SmeClassified)
    classification_dal.save_sme_classified()


def save_gem_classified():
    """获取创业板股票数据，即查找所有300开头的股票"""
    table_service.truncate_table(GemClassified)
    classification_dal.save_gem_classified()


def save_st_classified():
    """获取风险警示板股票数据，即查找所有st股票"""
    table_service.truncate_table(StClassified)
    classification_dal.save_st_classified()


def save_hs300s():
    """获取沪深300当前成份股及所占权重"""
    table_service.truncate_table(Hs300)
    classification_dal.save_hs300s()


def save_sz50s():
    """上证50成分股"""
    table_service.truncate_table(Sz50)
    classification_dal.save_sz50s()


def save_zz500s():
    """中证500成分股"""
    table_service.truncate_table(Zz500)
    classification_dal.save_zz500s()


def save_terminated():
    """获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    table_service.truncate_table(Terminated)
    classification_dal.save_terminated()


def save_suspend():
    """获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    table_service.truncate_table(Suspend)
    classification_dal.save_suspend()

