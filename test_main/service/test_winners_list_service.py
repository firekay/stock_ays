# encoding: UTF-8
from service import winners_list_service as wlservice
from test_main.constants import *
import test_main


def test_save_top_list():
    wlservice.save_top_list()


def test_save_individual_statistics_tops():
    wlservice.save_individual_statistics_tops()


def test_save_broker_tops():
    wlservice.save_broker_tops()


def test_save_institution_tops():
    wlservice.save_institution_tops()


def test_save_institution_detail():
    wlservice.save_institution_detail()

 
if __name__ == '__main__':
    test_main.setup_logging()
    test_save_top_list()
    test_save_individual_statistics_tops()
    test_save_broker_tops()
    test_save_institution_tops()
    test_save_institution_detail()
