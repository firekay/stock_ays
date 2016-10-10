# encoding: UTF-8

from peewee import *
from utils.mysql_utils import *
from utils.util import *
import tushare as ts


database = database
class BaseModel(Model):
    class Meta:
        database = database        


class HistoryData(BaseModel):
    """概念分类"""
    class Meta:
        db_table = 'history_data'

    code = CharField()
    name = CharField()    
    c_name = CharField()

    def create_industry_classified(self):
        connect()
        IndustryClassified.create_table()
        close()

    def save_industry_classified(self, type='sina'):
        data_df = ts.get_industry_classified(standard=type)
        print(data_df)
        data = data_df.values
        data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
        print(data)
        mutils.connect()
        IndustryClassified.insert_many(data_dicts).execute()
        mutils.close()
