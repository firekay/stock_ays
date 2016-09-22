import sys
sys.path.append('..')
from configparser import ConfigParser
from models import *

def __get_db(threadlocals=True, autocommit=True, 
                      fields=None, ops=None, 
                      autorollback=False, 
                      use_speedups=True):
    config = ConfigParser()
    config.read('resources/mysql.cfg')
    host = config.get('mysqld', 'host')
    port = config.get('mysqld', 'port')
    database = config.get('mysqld', 'database')
    user = config.get('mysqld', 'user')
    passwd = config.get('mysqld', 'passwd')
    print(host + port)
    print(user + passwd)
    return MySQLDatabase(database, host='localhost', user=user, passwd=passwd)    

database = __get_db()

def connect():
    database.connect()


def close():
    database.close()
    
    
def conn(fn):
    """执行前连接数据库，执行后注销"""
    def inner(fn):
        connect()
        fn()
        close()
    return inner(fn)



if __name__ == '__main__':
    database.connect()
    IndustryClassified.create_table()    
    database.close()