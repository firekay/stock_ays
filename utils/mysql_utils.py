# encoding: UTF-8

from configparser import ConfigParser
from peewee import *
from playhouse.pool import PooledMySQLDatabase

config = ConfigParser()
config.read('resources/db.cfg')
__host = config.get('mysqld', 'host')
__port = config.get('mysqld', 'port')
__db = config.get('mysqld', 'database')
__user = config.get('mysqld', 'user')
__passwd = config.get('mysqld', 'passwd')


def __get_db(threadlocals=True, autocommit=True, 
                      fields=None, ops=None, 
                      autorollback=False, 
                      use_speedups=True):
    config = ConfigParser()
    config.read('resources/db.cfg')
    host = config.get('mysqld', 'host')
    port = config.get('mysqld', 'port')
    db = config.get('mysqld', 'database')
    user = config.get('mysqld', 'user')
    passwd = config.get('mysqld', 'passwd')
    return MySQLDatabase(db, host=host, port=port, user=user, passwd=passwd)


def __get_pooled_db():
    return PooledMySQLDatabase(database=__db, max_connections=128,
                               stale_timeout=120, host=__host, port=int(__port),
                               user=__user, passwd=__passwd, charset='utf8')


database = __get_pooled_db()

# def connect():
#     database.connect()


def connect():
    return database.connect()


def close(con):
    if not con:
        database.close(con)
    
    
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
        con = connect()
        try:
            return fn(*args,**kargs)
        finally:
            if con:
                con.close()
    return inner


if __name__ == '__main__':
    database.connect()
    # IndustryClassified.create_table()
    database.close()
