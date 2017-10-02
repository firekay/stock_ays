# encoding: UTF-8
"""项目表的操作"""
# -*- coding:utf-8 -*-
import logging
from models.model import *

logger = logging.getLogger(__name__)


def truncate_table(model):
    """清空表
    
    参数为model中的类名。
    """
    logger.info('Truncate "table" %s' % model.__name__)
    model.truncate_table()


def create_table(model):
    """创建表。

    参数为model中的类名
    """
    logger.info('Create table %s.' % model.__name__)
    model.create_table()


def create_tables(classes):
    """参数为列表， 列表中数据是model中的类名"""
    assert classes, '要创建多个表的时候, 不能传入空列表'
    [create_table(model) for model in classes]


def drop_table(model):
    """删除单个表, 参数为model中的类名"""
    logger.info('Drop talbe %s.' % model.__name__)
    model.drop_table(fail_silently=True)


def drop_tables(classes):
    assert classes, '要删除多个表的时候, 不能传入空列表'
    """参数为列表， 列表中数据是model中的类名"""
    [drop_table(model) for model in classes]


def create_all_tables():
    # models必须是transaction_models, investment_ref_models...等定义的这些
    transaction_models = [HistoryKDataD, HistoryKDataW, HistoryKDataM, HistoryDataD,
                          HistoryDataW, HistoryDataM, RevoteHistoryData, TodayAllData,
                          TickData, BigIndexData, BigTradeData]
    investment_ref_models = [DistributionPlans, PerformanceForecast, RestrictedStock,
                             FundHoldings, NewStocks, FinancingSecuritiesSh,
                             FinancingSecuritiesDetailSh, FinancingSecuritiesSz,
                             FinancingSecuritiesDetailSz]
    classification_models = [IndustryClassified, ConceptClassified, SmeClassified,
                             AreaClassified, GemClassified, StClassified, Hs300, Sz50,
                             Zz500, Terminated, Suspend]
    base_models = [StockBasic, PerformanceReport, ProfitAbility, OperationAbility, GrowthAbility,
                   PayDebtAbility, CashFlow]
    macro_models = [DepositsRate, LoanRate, RequiredReservesRate, MoneySupply, MoneySupplyBal,
                    GrossDomesticProductYear, GrossDomesticProductQuarter, GdpThreeDemands,
                    GdpThreeIndustryPull, GdpThreeIndustryContrib, CPI, PPI]
    winners_list_models = [TopList, IndividualStatisticsTops, BrokerTops, InstitutionTops,
                           InstitutionDetail]
    bank_loan_models = [ShiborRate, ShiborQuote, ShiborMA, LPR, LprMA]
    logger.info('Begin create all tables.')

    logger.info('Begin create transaction tables.')
    create_tables(transaction_models)
    logger.info('End create transaction tables.')

    logger.info('Begin create investment tables.')
    create_tables(investment_ref_models)
    logger.info('End create classification tables.')

    logger.info('Begin create investment tables.')
    create_tables(classification_models)
    logger.info('End create classification tables.')

    logger.info('Begin create base tables.')
    create_tables(base_models)
    logger.info('End create base tables.')

    logger.info('Begin create macro tables.')
    create_tables(macro_models)
    logger.info('End create macro tables.')

    logger.info('Begin create winners_list tables.')
    create_tables(winners_list_models)
    logger.info('End create winners_list tables.')

    logger.info('Begin create bank_loan tables.')
    create_tables(bank_loan_models)
    logger.info('End create bank_loan tables.')

    logger.info('End create all tables.')


def drop_all_tables():
    # models必须是transaction_models, investment_ref_models...等定义的这些
    transaction_models = [HistoryKDataD, HistoryKDataW, HistoryKDataM, HistoryDataD,
                          HistoryDataW, HistoryDataM, RevoteHistoryData, TodayAllData,
                          TickData, BigIndexData, BigTradeData]
    investment_ref_models = [DistributionPlans, PerformanceForecast, RestrictedStock,
                             FundHoldings, NewStocks, FinancingSecuritiesSh,
                             FinancingSecuritiesDetailSh, FinancingSecuritiesSz,
                             FinancingSecuritiesDetailSz]
    classification_models = [IndustryClassified, ConceptClassified, SmeClassified,
                             AreaClassified, GemClassified, StClassified, Hs300, Sz50,
                             Zz500, Terminated, Suspend]
    base_models = [StockBasic, PerformanceReport, ProfitAbility, OperationAbility, GrowthAbility,
                   PayDebtAbility, CashFlow]
    macro_models = [DepositsRate, LoanRate, RequiredReservesRate, MoneySupply, MoneySupplyBal,
                    GrossDomesticProductYear, GrossDomesticProductQuarter, GdpThreeDemands,
                    GdpThreeIndustryPull, GdpThreeIndustryContrib, CPI, PPI]
    winners_list_models = [TopList, IndividualStatisticsTops, BrokerTops, InstitutionTops,
                           InstitutionDetail]
    bank_loan_models = [ShiborRate, ShiborQuote, ShiborMA, LPR, LprMA]

    logger.info('Begin drop all tables.')

    logger.info('Begin drop transaction tables.')
    drop_tables(transaction_models)
    logger.info('End drop transaction tables.')

    logger.info('Begin drop investment tables.')
    drop_tables(investment_ref_models)
    logger.info('End drop classification tables.')

    logger.info('Begin drop investment tables.')
    drop_tables(classification_models)
    logger.info('End drop classification tables.')

    logger.info('Begin drop base tables.')
    drop_tables(base_models)
    logger.info('End drop base tables.')

    logger.info('Begin drop macro tables.')
    drop_tables(macro_models)
    logger.info('End drop macro tables.')

    logger.info('Begin drop winners_list tables.')
    drop_tables(winners_list_models)
    logger.info('End drop winners_list tables.')

    logger.info('Begin drop bank_loan tables.')
    drop_tables(bank_loan_models)
    logger.info('End drop bank_loan tables.')

    logger.info('End drop all tables.')
