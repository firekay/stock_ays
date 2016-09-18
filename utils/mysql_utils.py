import sys
from configparser import ConfigParser

from peewee import *

def get_db(database, threadlocals=True, autocommit=True, 
                      fields=None, ops=None, 
                      autorollback=False, 
                      use_speedups=True):
    config = ConfigParser()
    config.read('../resources/mysql.cfg')
    host = config.get('mysqld', 'host')
    port = config.get('mysqld', 'port')
    user = config.get('mysqld', 'user')
    passwd = config.get('mysqld', 'passwd')
    print(host + port)
    print(user + passwd)
    sys.exit()
    return MySQLDatabase(database, host='localhost', user=user, passwd=passwd)    



if __name__ == '__main__':
    database = 'azkaban'
    get_db(database)