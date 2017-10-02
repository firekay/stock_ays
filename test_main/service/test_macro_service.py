# encoding: UTF-8
import test_main
from service import macro_service


def test_save_deposit_rate():
    macro_service.save_deposit_rate()


def test_save_loan_rate():
    macro_service.save_loan_rate()


def test_save_required_reserves_rate():
    macro_service.save_required_reserves_rate()


def test_save_money_supply():
    macro_service.save_money_supply()


def test_save_money_supply_bal():
    macro_service.save_money_supply_bal()


def test_save_gdp_year():
    macro_service.save_gdp_year()


def test_save_gdp_quarter():
    macro_service.save_gdp_quarter()


def test_save_gdp_three_demands():
    macro_service.save_gdp_three_demands()


def test_save_gdp_three_industry_pull():
    macro_service.save_gdp_three_industry_pull()


def test_save_gdp_three_industry_contrib():
    macro_service.save_gdp_three_industry_contrib()


def test_save_cpi():
    macro_service.save_cpi()


def test_save_ppi():
    macro_service.save_ppi()


if __name__ == '__main__':
    test_main.setup_logging()
    test_save_deposit_rate()
    test_save_loan_rate()
    test_save_required_reserves_rate()
    test_save_money_supply()
    test_save_money_supply_bal()
    test_save_gdp_year()
    test_save_gdp_quarter()
    test_save_gdp_three_demands()
    test_save_gdp_three_industry_pull()
    test_save_gdp_three_industry_contrib()
    test_save_cpi()
    test_save_ppi()
