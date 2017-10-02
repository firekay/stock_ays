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


def delete_year(model, year):
    logger.info('Begin delete %s data, year is: %s.' % (model.__name__, year))
    try:
        TopList.delete().where(model.date == date).execute()
    except Exception:
        logger.exception('Error delete %s data, year is: %s.' % (model.__name__, year))
        return False
    else:
        logger.info('Success delete %s data, year is: %s.' % (model.__name__, year))
        return True


def delete_date(model, date):
    logger.info('Begin delete %s data, insert date is: %s.' % (model.__name__, date))
    try:
        TopList.delete().where(model.date == date).execute()
    except Exception:
        logger.exception('Error delete %s data, insert date is: %s.' % (model.__name__, date))
        return False
    else:
        logger.info('Success delete %s data, insert date is: %s.' % (model.__name__, date))
        return True


def delete_insert_date_days_type_data(model, insert_date, days_type):
    """删除插入时间的数据
    
    Args:
        model: peewee定义的model, models.model.py中定义的
        insert_date: 插入时间
        days_type: 天的类型类型, e.g.: 5, 10, 30, 60
    """
    logger.info('Begin delete %s data, insert date is: %s.' % (model.__name__, insert_date))
    try:
        model.delete().where(model.insert_date == insert_date,
                             model.days_type == days_type)\
            .execute()
    except Exception:
        logger.exception('Error delete %s data, insert date is: %s.' % (model.__name__, insert_date))
        return False
    else:
        logger.info('Success delete %s data, insert date is: %s.' % (model.__name__, insert_date))
        return True


def delete_insert_date_data(model, insert_date):
    """删除插入时间的数据
    
    Args:
        model: peewee定义的model, models.model.py中定义的
        insert_date: 插入时间
    """
    logger.info('Begin delete %s data, insert date is: %s.' % (model.__name__, insert_date))
    try:
        model.delete().where(model.insert_date == insert_date).execute()
    except Exception:
        logger.exception('Error delete %s data, insert date is: %s.' % (model.__name__, insert_date))
        return False
    else:
        logger.info('Success delete %s data, insert date is: %s.' % (model.__name__, insert_date))
        return True


def save_data(model, data_dicts, year, quarter):
    """存储相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        year: 年份, YYYY格式
        quarter: 季度, 只能是1, 2, 3, 4
    """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save %s data, the year is: %s, quarter is: %s'
                % (model.__name__, year, quarter))
    try:
        model.insert_many(data_dicts).execute()
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
    """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save all %s data' % model.__name__)
    try:
        model.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save all %s data' % model.__name__)
        return False
    else:
        logger.info('Success save all %s data' % model.__name__)
        return True
