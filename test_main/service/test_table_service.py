# encoding: UTF-8

from service import table_service
from models.model import *


table_model = RestrictedStock
table_models = []


def test_create_table():
    table_service.create_table(table_model)


def test_create_tables():
    table_service.create_tables(table_models)


def test_drop_table():
    table_service.drop_table(table_model)


def test_drop_tables():
    table_service.drop_tables(table_models)

