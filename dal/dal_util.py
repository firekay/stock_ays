# encoding: UTF-8

from models.model import *
import logging
logger = logging.getLogger(__name__)


def delete_data(model, year, quarter):
    """删除相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        year: 年份, YYYY格式
        quarter: 季度, 只能是1, 2, 3, 4

    """
    logger.info('Begin delete %s data, the year is: %s, quarter is: %s'
                % (model.__name__, year, quarter))
    try:
        model.delete().where(model.year == year, model.quarter == quarter) \
            .execute()
    except Exception as e:
        logger.exception('Error delete %s data, the year is: %s, quarter is: %s'
                         % (model.__name__, year, quarter))
        return False
    else:
        logger.info('Success delete %s data, the year is: %s, quarter is: %s'
                    % (model.__name__, year, quarter))
        return True


def save_data(model, data_dicts, year, quarter):
    """存储相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        year: 年份, YYYY格式
        quarter: 季度, 只能是1, 2, 3, 4
    """
    assert not data_dicts.empty, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save %s data, the year is: %s, quarter is: %s'
                % (model.__name__, year, quarter))
    try:
        PerformanceReport.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save %s data, the year is: %s, quarter is: %s'
                         % (model.__name__, year, quarter))
        return False
    else:
        logger.info('Success save %s data, the year is: %s, quarter is: %s'
                    % (model.__name__, year, quarter))
        return True


def save_data(model, data_dicts):
    """存储数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        year: 年份, YYYY格式
        quarter: 季度, 只能是1, 2, 3, 4
    """
    assert not data_dicts.empty, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save all %s data' % model.__name__)
    try:
        PerformanceReport.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save all %s data' % model.__name__)
        return False
    else:
        logger.info('Success save all %s data' % model.__name__)
        return True
