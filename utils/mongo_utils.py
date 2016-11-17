# encoding: UTF-8

import sys
import pymongo
sys.path.append('..')
from configparser import ConfigParser
_client = None
def get_db():
    config = ConfigParser()
    config.read('resources/db.cfg')
    host = config.get('mongod', 'host')
    port = config.get('mongod', 'port')
    db = config.get('mongod', 'database')
    user = config.get('mongod', 'user')
    passwd = config.get('mongod', 'passwd')

    _client = pymongo.MongoClient(host, int(port))
    db = _client.stock_ays
    db.authenticate(user, passwd)

    return db

def close():
    if(_client is not None):
        _client.close()

if __name__ == '__main__':
    db = get_db()
    
    print(db.name)
    close()
