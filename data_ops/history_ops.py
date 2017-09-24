# encoding: UTF-8

import tushare as ts
from models import *
from utils.mysql_utils import *

#
# def save_industry_classified(type='sina'):
#     data_df = ts.get_industry_classified(standard=type)
#     print(data_df)
#     data = data_df.values
#     data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
#     print(data)
#     mutils.connect()
#     IndustryClassified.insert_many(data_dicts).execute()
#     mutils.close()
#
#
# @conn
# def save_concept_classified():
#     data_df = ts.get_concept_classified()
#     print(data_df)
#     data = data_df.values
#     data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
#     ConceptClassified.insert_many(data_dicts).execute()
#
#
# @conn
# def save_sme_classified():
#     data_df = ts.get_sme_classified()
#     print(data_df)
#     data = data_df.values
#     data_dicts = [ {'code': row[0], 'name': row[1], 'c_name': row[2]} for row in data ]
#     SmeClassified.insert_many(data_dicts).execute()
