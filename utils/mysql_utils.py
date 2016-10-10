# encoding: UTF-8

import sys
sys.path.append('..')
from configparser import ConfigParser
from peewee import *


def __get_db(threadlocals=True, autocommit=True, 
                      fields=None, ops=None, 
                      autorollback=False, 
                      use_speedups=True):
    config = ConfigParser()
    config.read('resources/mysql.cfg')
    host = config.get('mysqld', 'host')
    port = config.get('mysqld', 'port')
    db = config.get('mysqld', 'database')
    user = config.get('mysqld', 'user')
    passwd = config.get('mysqld', 'passwd')
    return MySQLDatabase(db, host='localhost', user=user, passwd=passwd)    

database = __get_db()

def connect():
    database.connect()


def close():
    database.close()
    
    
# def conn(fn):
#     """执行前连接数据库，执行后断开连接"""
#     def inner(*args,**kargs):
#         connect()
#         try:
#             return fn(*args,**kargs)
#         finally:
#             close()
#     return inner

def conn(fn):
    """执行前连接数据库，执行后断开连接"""
    def inner(*args,**kargs):
        connect()
        try:
            return fn(*args,**kargs)
        finally:
            if not database.is_closed():
                close()
    return inner




if __name__ == '__main__':
    database.connect()
    IndustryClassified.create_table()    
    database.close()
