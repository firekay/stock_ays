# encoding: UTF-8

from peewee import *
from utils.mysql_utils import *
from utils.util import *
import tushare as ts

database = database
class BaseModel(Model):
    class Meta:
        database = database        
        
class IndustryClassified(BaseModel):
    class Meta:
        db_table = 'industry_classified'
        
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

########################################################################
class ConceptClassified(BaseModel):
    """概念分类"""
    class Meta:
        db_table = 'concept_classified'
        
    code = CharField()
    name = CharField()    
    c_name = CharField()
        
    def create_concept_classified(self):
        @conn
        def create_table():
            ConceptClassified.create_table()
        
    def save_concept_classified(self):
        @conn
        def save_data():
            data_df = ts.get_concept_classified()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
            ConceptClassified.insert_many(data_dicts).execute()
    
    
########################################################################
class SmeClassified(BaseModel):
    """中小板分类"""
    class Meta:
        db_table = 'sme_classified'
        
    code = CharField()
    name = CharField()    
        
    def create_sme_classified(self):
        @conn
        def create_table():
            SmeClassified.create_table()
    
    def save_sme_classified(self):
        @conn
        def save_data():
            data_df = ts.get_sme_classified()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
            SmeClassified.insert_many(data_dicts).execute()

    
class AreaClassified(BaseModel):
    """地域分类"""
    class Meta:
        db_table = 'area_classified'
        
    code = CharField()
    name = CharField()    
    area = CharField()    
        
    def create_area_classified(self):
        @conn
        def create_table():
            AreaClassified.create_table()
    
    def save_area_classified(self):
        @conn
        def save_data():
            data_df = ts.get_area_classified()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1], 'area': row[2]} for row in data ]
            AreaClassified.insert_many(data_dicts).execute()

    
class GemClassified(BaseModel):
    """创业板分类"""
    class Meta:
        db_table = 'gem_classified'
        
    code = CharField()
    name = CharField()    
        
    def create_gem_classified(self):
        @conn
        def create_table():
            GemClassified.create_table()
    
    def save_gem_classified(self):
        @conn
        def save_data():
            data_df = ts.get_gem_classified()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
            GemClassified.insert_many(data_dicts).execute()

    
class StClassified(BaseModel):
    """风险警示板分类"""
    class Meta:
        db_table = 'st_classified'
        
    code = CharField()
    name = CharField()    
        
    def create_st_classified(self):
        @conn
        def create_table():
            StClassified.create_table()
    
    def save_st_classified(self):
        @conn
        def save_data():
            data_df = ts.get_st_classified()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
            StClassified.insert_many(data_dicts).execute()

            
class Hs300(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'hs300'
        
    code = CharField()
    name = CharField()    
    date = CharField()    
    weight = CharField()    
        
    def create_hs300s(self):
        @conn
        def create_table():
            Hs300.create_table()
    
    def save_hs300s(self):
        @conn
        def save_data():
            data_df = ts.get_hs300s()
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1], 'date': row[2], 'weight': row[3]} for row in data ]
            Hs300.insert_many(data_dicts).execute()


class Sz50(BaseModel):
    """上证50成分股"""
    class Meta:
        db_table = 'sz50'
        
    code = CharField()
    name = CharField()    
        
    def create_sz50s(self):
        @conn
        def create_table():
            Sz50.create_table()
    
    def save_sz50s(self):
        @conn
        def save_data():
            data_df = ts.get_sz50s()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
            Sz50.insert_many(data_dicts).execute()
            

class Zz500(BaseModel):
    """中证500成分股"""
    class Meta:
        db_table = 'zz500'
        
    code = CharField()
    name = CharField()    
        
    def create_zz500s(self):
        @conn
        def create_table():
            Zz500.create_table()
    
    def save_zz500s(self):
        @conn
        def save_data():
            data_df = ts.get_zz500s()    
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1]} for row in data ]
            Zz500.insert_many(data_dicts).execute()


class Terminated(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'terminated'
        
    code = CharField()
    name = CharField()    
    o_date = CharField()    
    t_date = CharField()    
    insert_date = CharField()    
        
    def create_terminated(self):
        @conn
        def create_table():
            Terminated.create_table()
    
    def save_terminated(self):
        @conn
        def save_data():
            today = str(get_today())
            data_df = ts.get_terminated()
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1], 'o_date': row[2], 't_date': row[3], 'insert_date': today} for row in data ]
            Terminated.insert_many(data_dicts).execute()


class Suspend(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'suspend'
        
    code = CharField()
    name = CharField()    
    o_date = CharField()    
    t_date = CharField()    
    insert_date = CharField()    
        
    def create_suspend(self):
        @conn
        def create_table():
            Suspend.create_table()
    
    def save_suspend(self):
        @conn
        def save_data():
            today = str(get_today())
            data_df = ts.get_terminated()
            print(data_df)    
            data = data_df.values
            data_dicts = [ {'code': row[0], 'name': row[1], 'o_date': row[2], 't_date': row[3], 'insert_date': today} for row in data ]
            Suspend.insert_many(data_dicts).execute()


