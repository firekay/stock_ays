# encoding: UTF-8
import test_main
from service import classfication_service as cservice


def test_save_industry_classified():
    cservice.save_industry_classified()


def test_save_concept_classified():
    cservice.save_concept_classified()


def test_save_area_classified():
    cservice.save_area_classified()


def test_save_sme_classified():
    cservice.save_sme_classified()


def test_save_gem_classified():
    cservice.save_gem_classified()


def test_save_st_classified():
    cservice.save_st_classified()


def test_save_hs300s():
    cservice.save_hs300s()


def test_save_sz50s():
    cservice.save_sz50s()


def test_save_zz500s():
    cservice.save_zz500s()


def test_save_terminated():
    cservice.save_terminated()


def test_save_suspend():
    cservice.save_suspend()


if __name__ == '__main__':
    test_main.setup_logging()
    test_save_industry_classified()

