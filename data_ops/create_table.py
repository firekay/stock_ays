# encoding: UTF-8

from peewee import *
from models import *
from utils.mysql_utils import *

        
    
def create_industry_classified():
    mutils.connect()
    IndustryClassified.create_table()
    mutils.close()
    

#----------------------------------------------------------------------
@conn
def create_concept_classified():
    ConceptClassified.create_table()
        
    
@conn
def create_sme_classified():
    SmeClassified.create_table()
