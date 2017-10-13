# encoding: UTF-8
"""项目表的操作"""
# -*- coding:utf-8 -*-
import logging
from models.model import *

logger = logging.getLogger(__name__)

transaction_models = [HistoryKDataD, HistoryKDataW, HistoryKDataM,
                      HistoryKData5, HistoryKData15, HistoryKData30, HistoryKData60,
                      HistoryDataD, HistoryDataW, HistoryDataM,
                      HistoryData5, HistoryData15, HistoryData30, HistoryData60,
                      RevoteHistoryData, TodayAllData,
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


def table2model(table):
    table_model = {
        'history_k_data_d': HistoryKDataD,
        'history_k_data_w': HistoryKDataW,
        'history_k_data_m': HistoryKDataM,
        'history_k_data_5': HistoryKData5,
        'history_k_data_15': HistoryKData15,
        'history_k_data_30': HistoryKData30,
        'history_k_data_60': HistoryKData60,
        'history_data_d': HistoryDataD,
        'history_data_w': HistoryDataW,
        'history_data_m': HistoryDataM,
        'history_data_5': HistoryData5,
        'history_data_15': HistoryData15,
        'history_data_30': HistoryData30,
        'history_data_60': HistoryData60,
        'revote_history_data': RevoteHistoryData,
        'today_all_data': TodayAllData,
        'tick_data': TickData,
        'big_index': BigIndexData,
        'big_trade_data': BigTradeData,

        'distribution_plans': DistributionPlans,
        'performance_forecast': PerformanceForecast,
        'restricted_stock': RestrictedStock,
        'fund_holdings': FundHoldings,
        'new_stocks': NewStocks,
        'financing_securities_sh': FinancingSecuritiesSh,
        'financing_securities_detail_sh': FinancingSecuritiesDetailSh,
        'financing_securities_sz': FinancingSecuritiesSz,
        'financing_securities_detail_sz': FinancingSecuritiesDetailSz,

        'industry_classified': IndustryClassified,
        'concept_classified': ConceptClassified,
        'sme_classified': SmeClassified,
        'area_classified': AreaClassified,
        'gem_classified': GemClassified,
        'st_classified': StClassified,
        'hs300': Hs300,
        'sz50': Sz50,
        'zz500': Zz500,
        'suspend': Suspend,

        'stock_basic': StockBasic,
        'performance_report': PerformanceReport,
        'profit_ability': ProfitAbility,
        'operation_ability': OperationAbility,
        'growth_ability': GrowthAbility,
        'pay_debt_ability': PayDebtAbility,
        'cash_flow': CashFlow,

        'deposits_rate': DepositsRate,
        'loan_rate': LoanRate,
        'required_reserves_rate': RequiredReservesRate,
        'money_supply': MoneySupply,
        'money_supply_bal': MoneySupplyBal,
        'gdp_year': GrossDomesticProductYear,
        'gdp_quarter': GrossDomesticProductQuarter,
        'gdp_three_demands': GdpThreeDemands,
        'gdp_three_industry_pull': GdpThreeIndustryPull,
        'gdp_three_industry_contrib': GdpThreeIndustryContrib,
        'cpi': CPI,
        'ppi': PPI,

        'top_list': TopList,
        'individual_statistics_tops': IndividualStatisticsTops,
        'broker_tops': BrokerTops,
        'institution_tops': InstitutionTops,
        'institution_detail': InstitutionDetail,

        'shibor_rate': ShiborRate,
        'shibor_quote': ShiborQuote,
        'lpr': LPR,
        'lpr_ma': LprMA
    }
    return table_model.get(table, None)


def truncate_table(model):
    """清空表
    
    参数为model中的类名。
    """
    logger.info('Truncate "table" %s' % model.__name__)
    model.truncate_table()


def create_tables_from_table_name(table_names):
    for table_name in table_names:
        model = table2model(table_name)
        if model:
            create_table(model)
        else:
            logger.error('Error create table, table name wrong, please check it, table name is %s.' % table_name)


def drop_tables_from_table_name(table_names):
    for table_name in table_names:
        model = table2model(table_name)
        if model:
            drop_table(model)
        else:
            logger.error('Error Drop table, table name wrong, please check it, table name is %s.' % table_name)


def create_table(model):
    """创建表。

    参数为model中的类名
    """
    logger.info('Create table %s.' % model.__name__)
    model.create_table()


def create_tables(models):
    """参数为列表， 列表中数据是model中的类名
    
    models必须是transaction_models, investment_ref_models...等定义的这些
    """
    assert models, '要创建多个表的时候, 不能传入空列表'
    [create_table(model) for model in models]


def drop_table(model):
    """删除单个表, 参数为model中的类名"""
    logger.info('Drop talbe %s.' % model.__name__)
    model.drop_table(fail_silently=True)


def drop_tables(models):
    """参数为列表， 列表中数据是model中的类名
    
    models必须是transaction_models, investment_ref_models...等定义的这些
    """
    assert models, '要删除多个表的时候, 不能传入空列表'
    [drop_table(model) for model in models]


def create_all_tables():
    # models必须是transaction_models, investment_ref_models...等定义的这些

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
