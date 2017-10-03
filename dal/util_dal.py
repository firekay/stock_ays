# encoding: UTF-8

from models.model import *
import logging
logger = logging.getLogger(__name__)


def delete_year_quarter_data(model, year, quarter):
    """删除相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        year: 年份, YYYY格式
        quarter: 季度, 只能是1, 2, 3, 4
    Returns:
        bool: if success delete, return True, else return False
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


def delete_year_month_data(model, year, month):
    """删除相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        year: 年份, YYYY格式
        month: 月份
    Returns:
        bool: if success delete, return True, else return False
    """
    logger.info('Begin delete %s data, the year is: %s, month is: %s'
                % (model.__name__, year, month))
    try:
        model.delete().where(model.year == year, model.month == month) \
            .execute()
    except Exception as e:
        logger.exception('Error delete %s data, the year is: %s, month is: %s'
                         % (model.__name__, year, month))
        return False
    else:
        logger.info('Success delete %s data, the year is: %s, month is: %s'
                    % (model.__name__, year, month))
        return True


def delete_year_data(model, year):
    """删除相应年份的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        year: 年份, YYYY格式
    Returns:
        bool: if success delete, return True, else return False
    """

    logger.info('Begin delete %s data, year is: %s.' % (model.__name__, year))
    year = str(year)
    try:
        model.delete().where(model.year == year).execute()
    except Exception:
        logger.exception('Error delete %s data, year is: %s.' % (model.__name__, year))
        return False
    else:
        logger.info('Success delete %s data, year is: %s.' % (model.__name__, year))
        return True


def delete_date_data(model, date):
    """删除相应天的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        date: 日期, model的字段名称必须为date
    Returns:
        bool: if success delete, return True, else return False
    """
    logger.info('Begin delete %s data, insert date is: %s.' % (model.__name__, date))
    try:
        model.delete().where(model.date == date).execute()
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
    Returns:
        bool: if success delete, return True, else return False
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
        insert_date: 插入时间, model的字段名必须为insert_date
    Returns:
        bool: if success delete, return True, else return False
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


def save_year_data(model, data_dicts, year):
    """存储相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        year: 年份, YYYY格式
        quarter: 季度, 只能是1, 2, 3, 4
    """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save %s data, the year is: %s'
                % (model.__name__, year))
    try:
        model.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save %s data, the year is: %s'
                         % (model.__name__, year))
        return False
    else:
        logger.info('Success save %s data, the year is: %s'
                    % (model.__name__, year))
        return True


def save_year_quarter_data(model, data_dicts, year, quarter):
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


def save_year_month_data(model, data_dicts, year, month):
    """存储相应年份,季度的数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        year: 年份, YYYY格式
        month: 月份
    """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save %s data, the year is: %s, month is: %s'
                % (model.__name__, year, month))
    try:
        model.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save %s data, the year is: %s, month is: %s'
                         % (model.__name__, year, month))
        return False
    else:
        logger.info('Success save %s data, the year is: %s, month is: %s'
                    % (model.__name__, year, month))
        return True


def save_date_day_type_data(model, data_dicts, date, day_type):
    """存储数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        date: 日期
        day_type: 天统计的类型
    """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save %s data, date is: %s, day_type is: %s'
                % (model.__name__, date, day_type))
    try:
        model.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save %s data, date is: %s, day_type is: %s'
                         % (model.__name__, date, day_type))
        return False
    else:
        logger.info('Success save %s data, date is: %s, day_type is: %s' %
                    (model.__name__, date, day_type))
        return True


def save_date_data(model, data_dicts, date):
    """存储数据

    Args:
        model: peewee定义的model, models.model.py中定义的
        data_dicts: 字典的列表, 跟model对应的数据
        date: 日期
    """
    assert data_dicts, 'data_dict must not empty and data_dict must not None'
    logger.info('Begin save %s data, date is: %s' % (model.__name__, date))
    try:
        model.insert_many(data_dicts).execute()
    except Exception as e:
        logger.exception('Error save %s data, date is: %s' % (model.__name__, date))
        return False
    else:
        logger.info('Success save %s data, date is: %s' % (model.__name__, date))
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
