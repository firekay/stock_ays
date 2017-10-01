# encoding: UTF-8
"""项目表的操作"""
# -*- coding:utf-8 -*-
import logging
from models.model import *

logger = logging.getLogger(__name__)


def truncate_table(model):
    """清空表
    
    参数为model中的类名。
    """
    logger.info('Truncate "table" %s' % model.__name__)
    model.truncate_table()


def create_table(model):
    """创建表。

    参数为model中的类名
    """
    logger.info('Create table %s.' % model.__name__)
    model.create_table()


def create_tables(classes):
    """参数为列表， 列表中数据是model中的类名"""
    [create_table(model) for model in classes]


def drop_table(model):
    """删除单个表, 参数为model中的类名"""
    logger.info('Drop talbe %s.' % model.__name__)
    model.drop_table(fail_silently=True)


def drop_tables(classes):
    """参数为列表， 列表中数据是model中的类名"""
    [drop_table(model) for model in classes]


def create_all_tables():
    logger.info('Begin create all tables.')
    cls_models = [IndustryClassified, ConceptClassified, SmeClassified,
                  AreaClassified, GemClassified, StClassified,
                  Hs300, Sz50, Zz500, Terminated, Suspend,
                  StockBasic, HistoryDataD, HistoryDataW, HistoryDataM, HistoryDataScd,
                  RevoteHistoryData, TodayAllData, TickData,
                  BigIndexData, BigTradeData]
    create_tables(cls_models)
    logger.info('Begin end all tables.')


def drop_all_tables():
    logger.info('Begin drop all tables.')
    cls_models = [IndustryClassified, ConceptClassified, SmeClassified,
                  AreaClassified, GemClassified, StClassified,
                  Hs300, Sz50, Zz500, Terminated, Suspend,
                  StockBasic, HistoryDataD, HistoryDataW, HistoryDataM, HistoryDataScd,
                  RevoteHistoryData, TodayAllData, TickData,
                  BigIndexData, BigTradeData]
    drop_tables(cls_models)
    logger.info('End drop all tables.')
