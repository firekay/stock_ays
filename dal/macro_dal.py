# encoding: UTF-8

from models.model import *
import tushare as ts
import logging

logger = logging.getLogger(__name__)

ts.get_deposit_rate()


def get_deposit_rate():
    """得到存款利率"""
    logger.info('Begin get DepositsRate.')
    try:
        data_df = ts.get_deposit_rate()
    except Exception as e:
        logger.exception('Error get DepositsRate.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get DepositsRate.')
        else:
            data_dicts = [{'date': row[0], 'deposit_type': row[1], 'rate': row[2]} for row in data_df.values]
            logger.info('End get DepositsRate.')
        return data_dicts


def get_loan_rate():
    """得到贷款利率"""
    logger.info('Begin get LoanRate.')
    try:
        data_df = ts.get_loan_rate()
    except Exception as e:
        logger.exception('Error get LoanRate.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get LoanRate.')
        else:
            data_dicts = [{'date': row[0], 'loan_type': row[1], 'rate': row[2]} for row in data_df.values]
            logger.info('End get LoanRate.')
        return data_dicts


def get_required_reserves_rate():
    """得到存款准备金率"""
    logger.info('Begin get RequiredReservesRate.')
    try:
        data_df = ts.get_rrr()
    except Exception as e:
        logger.exception('Error get RequiredReservesRate.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get RequiredReservesRate.')
        else:
            data_dicts = [{'date': row[0], 'before': row[1], 'now': row[2], 'changed': row[3]}
                          for row in data_df.values]
            logger.info('End get RequiredReservesRate.')
        return data_dicts


def get_money_supply():
    """得到货币供应量"""
    logger.info('Begin get MoneySupply.')
    try:
        data_df = ts.get_money_supply()
    except Exception as e:
        logger.exception('Error get MoneySupply.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get MoneySupply.')
        else:
            data_dicts = [{'month': row[0], 'm2': row[1],
                           'm2_yoy': row[2], 'm1': row[3], 'm1_yoy': row[4],
                           'm0': row[5], 'm0_yoy': row[6], 'cd': row[7], 'cd_yoy': row[8],
                           'qm': row[9], 'qm_yoy': row[10], 'ftd': row[11], 'ftd_yoy': row[12],
                           'sd':row[13], 'sd_yoy':row[14], 'rests': row[15], 'rests_yoy': row[16]}
                          for row in data_df.values]
            logger.info('End get MoneySupply.')
        return data_dicts


def get_money_supply_bal():
    """得到货币供应量(年底余额)"""
    logger.info('Begin get MoneySupplyBal.')
    try:
        data_df = ts.get_money_supply_bal()
    except Exception as e:
        logger.exception('Error get MoneySupplyBal.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get MoneySupplyBal.')
        else:
            data_dicts = [{'year': row[0], 'm2': row[1],
                           'm1': row[2], 'm0': row[3], 'cd': row[4],
                           'qm': row[5], 'ftd': row[6], 'sd': row[7], 'rests': row[8]}
                          for row in data_df.values]
            logger.info('End get MoneySupplyBal.')
        return data_dicts


def get_gdp_year():
    """国内生产总值(年度)"""
    logger.info('Begin get GrossDomesticProductYear.')
    try:
        data_df = ts.get_gdp_year()
    except Exception as e:
        logger.exception('Error get GrossDomesticProductYear.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get GrossDomesticProductYear.')
        else:
            data_dicts = [{'year': row[0], 'gdp': row[1],
                           'pc_gdp': row[2], 'gnp': row[3], 'pi': row[4],
                           'si': row[5], 'industry': row[6], 'cons_industry': row[7], 'ti': row[8],
                           'trans_industry': row[9], 'lbdy': row[10]}
                          for row in data_df.values]
            logger.info('End get GrossDomesticProductYear.')
        return data_dicts


def get_gdp_quarter():
    """得到国内生产总值(季度)"""
    logger.info('Begin get GrossDomesticProductQuarter.')
    try:
        data_df = ts.get_gdp_quarter()
    except Exception as e:
        logger.exception('Error get GrossDomesticProductQuarter.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get GrossDomesticProductQuarter.')
        else:
            data_dicts = [{'quarter': row[0], 'gdp': row[1],
                           'gdp_yoy': row[2], 'pi': row[3], 'pi_yoy': row[4],
                           'si': row[5], 'si_yoy': row[6], 'ti': row[7], 'ti_yoy': row[8]}
                          for row in data_df.values]
            logger.info('End get GrossDomesticProductQuarter.')
        return data_dicts


def get_gdp_three_demands():
    """三大需求对GDP贡献"""
    logger.info('Begin get GdpThreeDemands.')
    try:
        data_df = ts.get_gdp_for()
    except Exception as e:
        logger.exception('Error get GdpThreeDemands.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get GdpThreeDemands.')
        else:
            data_dicts = [{'year': row[0], 'end_for': row[1],
                           'for_rate': row[2], 'asset_for': row[3], 'asset_rate': row[4],
                           'goods_for': row[5], 'goods_rate': row[6]}
                          for row in data_df.values]
            logger.info('End get GdpThreeDemands.')
        return data_dicts


def get_gdp_three_industry_pull():
    """三大产业对GDP拉动"""
    logger.info('Begin get GdpThreeIndustryPull.')
    try:
        data_df = ts.get_gdp_pull()
    except Exception as e:
        logger.exception('Error get GdpThreeIndustryPull.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get GdpThreeIndustryPull.')
        else:
            data_dicts = [{'year': row[0], 'gdp_yoy': row[1], 'pi': row[2], 'si': row[3],
                           'industry': row[4], 'ti': row[5]}
                          for row in data_df.values]
            logger.info('End get GdpThreeIndustryPull.')
        return data_dicts


def get_gdp_three_industry_contrib():
    """三大产业贡献率"""
    logger.info('Begin get GdpThreeIndustryContrib.')
    try:
        data_df = ts.get_gdp_contrib()
    except Exception as e:
        logger.exception('Error get GdpThreeIndustryContrib.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get GdpThreeIndustryContrib.')
        else:
            data_dicts = [{'year': row[0], 'gdp_yoy': row[1],
                           'pi': row[2], 'si': row[3], 'industry': row[4],
                           'ti': row[5]}
                          for row in data_df.values]
            logger.info('End get GdpThreeIndustryContrib.')
        return data_dicts


def get_cpi():
    """居民消费价格指数"""
    logger.info('Begin get CPI.')
    try:
        data_df = ts.get_cpi()
    except Exception as e:
        logger.exception('Error get CPI.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get CPI.')
        else:
            data_dicts = [{'month': row[0], 'cpi': row[1]} for row in data_df.values]
            logger.info('End get CPI.')
        return data_dicts


def get_ppi():
    """工业品出厂价格指数"""
    logger.info('Begin get PPI.')
    try:
        data_df = ts.get_ppi()
    except Exception as e:
        logger.exception('Error get PPI.')
        return None
    else:
        data_dicts = []
        if data_df.empty:
            logger.warn('Empty get PPI.')
        else:
            data_dicts = [{'month': row[0], 'ppiip': row[1],
                           'ppi': row[2], 'qm': row[3], 'rmi': row[4],
                           'pi': row[5], 'cg': row[6], 'food': row[7], 'clothing': row[8],
                           'roeu': row[9], 'dcg': row[10]}
                          for row in data_df.values]

            logger.info('End get PPI.')
        return data_dicts

