# encoding: UTF-8

from service import table_service
from models.model import *


table_model = DistributionPlans

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


def test_create_table():
    table_service.create_table(table_model)


def test_drop_table():
    table_service.drop_table(table_model)


def test_create_tables():
    table_service.create_tables(investment_ref_models)


def test_drop_tables():
    table_service.drop_tables(investment_ref_models)


def test_drop_all_tables():
    table_service.drop_all_tables()

