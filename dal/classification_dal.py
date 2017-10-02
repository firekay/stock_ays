# encoding: UTF-8

import logging.config
import tushare as ts
from models.model import *

logger = logging.getLogger(__name__)
today_line = get_today_line()


def delete_industry_classified():
    delete_ok = True
    logger.info('Begin delete industry classified行业信息.')
    try:
        IndustryClassified.delete().execute()
    except Exception:
        delete_ok = False
        logger.exception('Error delete industry classified行业信息.')
    else:
        logger.info('Success delete industry classified行业信息.')
    return delete_ok


def save_industry_classified():
    """在现实交易中，经常会按行业统计股票的涨跌幅或资金进出，本接口按照sina财经对沪深股票进行的行业分类，返回所有股票所属行业的信息。"""
    logger.info('Begin get and save industry classified行业信息.')
    try:
        data_df = ts.get_industry_classified(standard=type)
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data]
        IndustryClassified.insert_many(data_dicts).execute()
        logger.info('End get and save industry classified行业信息.')
    except Exception as e:
        logger.exception('Error get and save industry classified行业信息.')


def save_concept_classified():
    """返回股票概念的分类数据，现实的二级市场交易中，经常会以”概念”来炒作，在数据分析过程中，可根据概念分类监测资金等信息的变动情况。"""
    logger.info('Begin get and save concept clssified股票概念的分类数据.')
    try:
        data_df = ts.get_concept_classified()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data]
        ConceptClassified.insert_many(data_dicts).execute()
        logger.info('End get and save concept clssified股票概念的分类数据.')
    except Exception as e:
        logger.exception('Error get and save concept clssified股票概念的分类数据.')


def save_area_classified():
    """按地域对股票进行分类，即查找出哪些股票属于哪个省份。"""
    logger.info('Begin get and save area clssified.')
    try:
        data_df = ts.get_area_classified()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'area': row[2]} for row in data]
        AreaClassified.insert_many(data_dicts).execute()
        logger.info('End get and save area clssified.')
    except Exception as e:
        logger.exception('Error get and save area clssified.')


def save_sme_classified():
    """获取中小板股票数据，即查找所有002开头的股票"""
    logger.info('Begin get and save sme中小板 clssified.')
    try:
        data_df = ts.get_sme_classified()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1]} for row in data]
        SmeClassified.insert_many(data_dicts).execute()
        logger.info('End get and save sme中小板 classified.')
    except Exception as e:
        logger.exception('Error get and save sme中小板 classified.')


def save_gem_classified():
    """获取创业板股票数据，即查找所有300开头的股票"""
    logger.info('Begin get and save gem 创业板股票数据clssified.')
    try:
        data_df = ts.get_gem_classified()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1]} for row in data]
        GemClassified.insert_many(data_dicts).execute()
        logger.info('End get and save gem 创业板股票数据classified.')
    except Exception as e:
        logger.exception('Error get and save gem 创业板股票数据classified.')


def save_st_classified():
    """获取风险警示板股票数据，即查找所有st股票"""
    logger.info('Begin get and save st clssified.')
    try:
        data_df = ts.get_st_classified()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1]} for row in data]
        StClassified.insert_many(data_dicts).execute()
        logger.info('End get and save st classified.')
    except Exception as e:
        logger.exception('Error get and save st classified.')


def save_hs300s():
    """获取沪深300当前成份股及所占权重"""
    logger.info('Begin get and save hs300 clssified.')
    try:
        data_df = ts.get_hs300s()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'date': row[2], 'weight': row[3]} for row in data]
        Hs300.insert_many(data_dicts).execute()
        logger.info('End get and save hs300 classified.')
    except Exception as e:
        logger.exception('Error get and save hs300 classified.')


def save_sz50s():
    """上证50成分股"""
    logger.info('Begin get and save sz50 clssified.')
    try:
        data_df = ts.get_sz50s()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1]} for row in data]
        Sz50.insert_many(data_dicts).execute()
        logger.info('End get and save sz50 classified.')
    except Exception as e:
        logger.exception('Error get and save sz50 classified.')


def save_zz500s():
    """中证500成分股"""
    logger.info('Begin get and save zz500 clssified.')
    try:
        data_df = ts.get_zz500s()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1]} for row in data]
        Zz500.insert_many(data_dicts).execute()
        logger.info('End get and save zz500 classified.')
    except Exception as e:
        logger.exception('Error get and save zz500 classified.')


def save_terminated():
    """获取已经被终止上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    logger.info('Begin get and save terminated clssified.')
    try:
        data_df = ts.get_terminated()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'o_date': row[2], 't_date': row[3],
                       'insert_date': today_line} for row in data]
        Terminated.insert_many(data_dicts).execute()
        logger.info('End get and save terminated classified.')
    except Exception as e:
        logger.exception('Error get and save terminated classified.')


def save_suspend():
    """获取被暂停上市的股票列表，数据从上交所获取，目前只有在上海证券交易所交易被终止的股票。"""
    logger.info('Begin get and save suspend clssified.')
    try:
        data_df = ts.get_terminated()
        data = data_df.values
        data_dicts = [{'code': row[0], 'name': row[1], 'o_date': row[2], 't_date': row[3],
                       'insert_date': today_line} for row in data]
        Suspend.insert_many(data_dicts).execute()
        logger.info('End get and save suspend classified.')
    except Exception as e:
        logger.exception('Error get and save suspend classified.')
