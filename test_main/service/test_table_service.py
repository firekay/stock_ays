# encoding: UTF-8

from service import table_service
from models.model import *


table_model = TodayAllData

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


models = transaction_models


def test_table2model(table):
    model = table_service.table2model(table)
    print(type(model))
    print(model)


def test_create_table():
    table_service.create_table(table_model)


def test_drop_table():
    table_service.drop_table(table_model)


def test_create_tables():
    table_service.create_tables(models)


def test_drop_tables():
    table_service.drop_tables(models)


def test_drop_all_tables():
    table_service.drop_all_tables()


if __name__ == '__main__':
    test_table2model('concept_classified')

    # test_drop_table()
    # test_create_table()

    # test_drop_tables()
    # test_create_tables()