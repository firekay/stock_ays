
from configparser import ConfigParser
import tushare as ts
from peewee import *


config = ConfigParser()
config.read('resources/mysql.cfg')
host = config.get('mysqld', 'host')
port = config.get('mysqld', 'port')
database = config.get('mysqld', 'database')
user = config.get('mysqld', 'user')
passwd = config.get('mysqld', 'passwd')
print(host + port)
print(user + passwd)
database = MySQLDatabase(database, host='localhost', user=user, passwd=passwd)    
class BaseModel(Model):
    class Meta:
        database = database        
        
class IndustryClassified(BaseModel):
    type = CharField(max_length=30)    
    code = IntegerField()    
    name = CharField(max_length=255)    
    c_name = CharField()    
    
database.connect()
IndustryClassified.create_table()