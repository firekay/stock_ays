# encoding: UTF-8

from utils.mysql_utils import *
from utils.util import *


today = str(get_today())


class BaseModel(Model):
    class Meta:
        database = database


# #####################################################
# 交易数据
# #####################################################
# 历史交易数据: 天
class HistoryKDataD(BaseModel):
    """历史行情: D"""
    class Meta:
        db_table = 'history_k_data_d'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    autype = CharField(5)  # 复权类型: qfq-前复权 hfq-后复权 None-不复权，默认为qfq
    open = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)


class HistoryKDataW(BaseModel):
    """历史行情: 周"""
    class Meta:
        db_table = 'history_k_data_d'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    autype = CharField(5)  # 复权类型: qfq-前复权 hfq-后复权 None-不复权，默认为qfq
    open = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)


class HistoryKDataM(BaseModel):
    """历史行情: 月"""
    class Meta:
        db_table = 'history_k_data_d'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    autype = CharField(5)  # 复权类型: qfq-前复权 hfq-后复权 None-不复权，默认为qfq
    open = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)


class HistoryDataD(BaseModel):
    """历史行情: D"""
    class Meta:
        db_table = 'history_data_d'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 = DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=10, decimal_places=2)


# 历史交易数据: 周
class HistoryDataW(BaseModel):
    """历史行情:  W"""
    class Meta:
        db_table = 'history_data_w'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 = DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=10, decimal_places=2)


# 历史交易数据: 月
class HistoryDataM(BaseModel):
    """历史行情:  M"""
    class Meta:
        db_table = 'history_data_m'

    code = CharField(8)
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    price_change = DecimalField(max_digits=10, decimal_places=2)
    p_change = DecimalField(max_digits=10, decimal_places=2)
    ma5 = DecimalField(max_digits=10, decimal_places=3)
    ma10 = DecimalField(max_digits=10, decimal_places=4)
    ma20 = DecimalField(max_digits=10, decimal_places=4)
    v_ma5 = DecimalField(max_digits=12, decimal_places=2)
    v_ma10 = DecimalField(max_digits=12, decimal_places=2)
    v_ma20 = DecimalField(max_digits=12, decimal_places=2)
    turnover = DecimalField(max_digits=10, decimal_places=2)


class RevoteHistoryData(BaseModel):
    """复权数据"""
    # get_h_data
    class Meta:
        db_table = 'revote_history_data'

    code = CharField()
    autype = CharField(5)  # 复权类型: qfq-前复权 hfq-后复权 None-不复权，默认为qfq
    date = DateField('%Y-%m-%d')
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    close = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    amount = DecimalField(max_digits=15, decimal_places=2)


class TodayAllData(BaseModel):
    """实时行情"""
    class Meta:
        db_table = 'today_all_data'

    code = CharField()
    name = CharField()
    date = DateField('%Y-%m-%d')
    changepercent = DecimalField(max_digits=8, decimal_places=3)
    trade = DecimalField(max_digits=8, decimal_places=2)
    open = DecimalField(max_digits=8, decimal_places=2)
    hign = DecimalField(max_digits=8, decimal_places=2)
    low = DecimalField(max_digits=8, decimal_places=2)
    settlement = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=12, decimal_places=2)
    turnoverratio = DecimalField(max_digits=8, decimal_places=5)
    amount = DecimalField(max_digits=15, decimal_places=2)
    per = DecimalField(max_digits=10, decimal_places=4)
    pb = DecimalField(max_digits=10, decimal_places=4)
    mktcap = DecimalField(max_digits=15, decimal_places=2)
    nmc = DecimalField(max_digits=15, decimal_places=2)


class TickData(BaseModel):
    """历史分笔, 当日历史分笔"""
    class Meta:
        db_table = 'tick_data'

    code = CharField()
    date = DateField('%Y-%m-%d')
    time = TimeField('%H:%M:%S')
    price = DecimalField(max_digits=8, decimal_places=2)
    pchange = DecimalField(max_digits=5, decimal_places=2)
    change = DecimalField(max_digits=5, decimal_places=2)
    volume = DecimalField(max_digits=10, decimal_places=2)
    amount = DecimalField(max_digits=12, decimal_places=2)
    type = CharField()


class BigIndexData(BaseModel):
    """大盘指数行情列表"""
    class Meta:
        db_table = 'big_index'

    date = DateField('%Y-%m-%d')
    code = CharField()
    name = CharField()
    change = DecimalField(max_digits=5, decimal_places=2)
    open = DecimalField(max_digits=12, decimal_places=4)
    preclose = DecimalField(max_digits=12, decimal_places=4)
    close = DecimalField(max_digits=12, decimal_places=4)
    hign = DecimalField(max_digits=12, decimal_places=4)
    low = DecimalField(max_digits=12, decimal_places=4)
    volume = DecimalField(max_digits=10, decimal_places=2)
    amount = DecimalField(max_digits=12, decimal_places=4)


class BigTradeData(BaseModel):
    """大单交易数据"""
    class Meta:
        db_table = 'big_trade_data'

    date = DateField('%Y-%m-%d')
    code = CharField()
    name = CharField()
    time = TimeField('%H:%M:%S')
    price = DecimalField(max_digits=8, decimal_places=2)
    volume = DecimalField(max_digits=10, decimal_places=2)
    preprice = DecimalField(max_digits=8, decimal_places=2)
    type = CharField()


# #####################################################
# 投资参考数据
# #####################################################
class DistributionPlans(BaseModel):
    """分配预案"""
    class Meta:
        db_table = 'distribution_plans'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    report_date = DateField('%Y-%m-%d')
    divi = CharField(32)
    shares = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class PerformanceForecast(BaseModel):
    """业绩预告"""
    class Meta:
        db_table = 'performance_forecast'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    type = CharField(32)
    report_date = DateField('%Y-%m-%d')
    pre_eps = CharField(32)
    range = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class RestrictedStock(BaseModel):
    """限售股解禁"""
    class Meta:
        db_table = 'restricted_stock'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    month = CharField(2)
    date = DateField('%Y-%m-%d')
    count = CharField(32)
    ratio = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class FundHoldings(BaseModel):
    """基金持股"""
    class Meta:
        db_table = 'fund_holdings'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    date = DateField('%Y-%m-%d')
    nums = CharField(32)
    nlast = CharField(32)
    count = CharField(32)
    clast = CharField(32)
    amount = CharField(32)
    ratio = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class NewStocks(BaseModel):
    class Meta:
        db_table = 'new_stocks'

    code = CharField(8)
    xcode = CharField(8)
    name = CharField(32)
    ipo_date = DateField('%Y-%m-%d')
    issue_date = CharField(32)
    amount = CharField(32)
    markets = CharField(32)
    price = CharField(32)
    pe = CharField(32)
    limit = CharField(32)
    funds = CharField(32)
    ballot = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class FinancingSecuritiesSh(BaseModel):
    """沪市融资融券"""
    class Meta:
        db_table = 'financing_securities_sh'

    op_date = DateField('%Y-%m-%d')
    rzye = CharField(32)
    rzmre = CharField(32)
    rqyl = CharField(32)
    rqylje = CharField(32)
    rqmcl = CharField(32)
    rzrqjyzl = CharField(32)


class FinancingSecuritiesDetailSh(BaseModel):
    """沪市融资融券明细"""
    class Meta:
        db_table = 'financing_securities_detail_sh'

    op_date = DateField('%Y-%m-%d')
    stock_code = CharField(8)
    security_abbr = CharField(32)
    rzye = CharField(32)
    rzmre = CharField(32)
    rzche = CharField(32)
    rqyl = CharField(32)
    rqmcl = CharField(32)
    rqchl = CharField(32)


class FinancingSecuritiesSz(BaseModel):
    """深市融资融券"""
    class Meta:
        db_table = 'financing_securities_sz'

    op_date = DateField('%Y-%m-%d')
    rzmre = CharField(32)
    rzye = CharField(32)
    rqmcl = CharField(32)
    rqyl = CharField(32)
    rqye = CharField(32)
    rzrqye = CharField(32)


class FinancingSecuritiesDetailSz(BaseModel):
    """深市融资融券明细"""
    class Meta:
        db_table = 'financing_securities_detail_sz'

    op_date = DateField('%Y-%m-%d')
    stock_code = CharField(8)
    security_abbr = CharField(32)
    rzmre = CharField(32)
    rzye = CharField(32)
    rqmcl = CharField(32)
    rqyl = CharField(32)
    rqye = CharField(32)
    rzrqye = CharField(32)


# #####################################################
# 股票分类数据
# #####################################################
class IndustryClassified(BaseModel):
    class Meta:
        db_table = 'industry_classified'
        
    code = CharField()
    name = CharField()    
    c_name = CharField()


class ConceptClassified(BaseModel):
    """概念分类"""
    class Meta:
        db_table = 'concept_classified'
 
    code = CharField()
    name = CharField()    
    c_name = CharField()
    
    
class SmeClassified(BaseModel):
    """中小板分类"""
    class Meta:
        db_table = 'sme_classified'
        
    code = CharField()
    name = CharField()    


class AreaClassified(BaseModel):
    """地域分类"""
    class Meta:
        db_table = 'area_classified'
 
    code = CharField()
    name = CharField()    
    area = CharField()    

    
class GemClassified(BaseModel):
    """创业板分类"""
    class Meta:
        db_table = 'gem_classified'
        
    code = CharField()
    name = CharField()    

    
class StClassified(BaseModel):
    """风险警示板分类"""
    class Meta:
        db_table = 'st_classified'
        
    code = CharField()
    name = CharField()    


class Hs300(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'hs300'
        
    code = CharField()
    name = CharField()    
    date = CharField()    
    weight = CharField()    


class Sz50(BaseModel):
    """上证50成分股"""
    class Meta:
        db_table = 'sz50'
        
    code = CharField()
    name = CharField()    
 

class Zz500(BaseModel):
    """中证500成分股"""
    class Meta:
        db_table = 'zz500'
        
    code = CharField(8)
    name = CharField(32)


class Terminated(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'terminated'
        
    code = CharField()
    name = CharField()    
    o_date = CharField()    
    t_date = CharField()    
    insert_date = CharField()    


class Suspend(BaseModel):
    """沪深300成分及权重"""
    class Meta:
        db_table = 'suspend'
        
    code = CharField()
    name = CharField()    
    o_date = CharField()    
    t_date = CharField()    
    insert_date = CharField()    


# #####################################################
# 基本面数据
# #####################################################
class StockBasic(BaseModel):
    """股票列表"""
    class Meta:
        db_table = 'stock_basic'

    code = CharField(8)
    name = CharField()
    industry = CharField()
    area = CharField()
    pe = DecimalField(max_digits=12, decimal_places=2)
    outstanding = DecimalField(max_digits=12, decimal_places=2)
    totals = DecimalField(max_digits=12, decimal_places=2)
    totalAssets = DecimalField(max_digits=12, decimal_places=2)
    liquidAssets = DecimalField(max_digits=12, decimal_places=2)
    fixedAssets = DecimalField(max_digits=12, decimal_places=2)
    reserved = DecimalField(max_digits=12, decimal_places=2)
    reservedPerShare = DecimalField(max_digits=12, decimal_places=2)
    eps = DecimalField(max_digits=12, decimal_places=3)
    bvps = DecimalField(max_digits=12, decimal_places=2)
    pb = DecimalField(max_digits=12, decimal_places=2)
    timeToMarket = IntegerField()
    undp = DecimalField(max_digits=12, decimal_places=2)
    perundp = DecimalField(max_digits=12, decimal_places=2)
    rev = DecimalField(max_digits=12, decimal_places=2)
    profit = DecimalField(max_digits=12, decimal_places=2)
    gpr = DecimalField(max_digits=12, decimal_places=2)
    npr = DecimalField(max_digits=12, decimal_places=2)
    holders = DecimalField(max_digits=12, decimal_places=2)
    insert_date = DateField('%Y-%m-%d')


class PerformanceReport(BaseModel):
    """业绩报告(主表)"""
    class Meta:
        db_table = 'performance_report'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField()
    eps = CharField(32)
    eps_yoy = CharField(32)
    bvps = CharField(32)
    roe = CharField(32)
    epcf = CharField(32)
    net_profits = CharField(32)
    profits_yoy = CharField(32)
    distrib = CharField(32)
    report_date = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class ProfitAbility(BaseModel):
    """盈利能力"""
    class Meta:
        db_table = 'profit_ability'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    roe = CharField(32)
    net_profit_ratio = CharField(32)
    gross_profit_rate = CharField(32)
    net_profits = CharField(32)
    esp = CharField(32)
    business_income = CharField(32)
    bips = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class OperationAbility(BaseModel):
    """营运能力"""
    class Meta:
        db_table = 'operation_ability'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    arturnover = CharField(32)
    arturndays = CharField(32)
    inventory_turnover = CharField(32)
    inventory_days = CharField(32)
    currentasset_turnover = CharField(32)
    currentasset_days = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class GrowthAbility(BaseModel):
    """成长能力"""
    class Meta:
        db_table = 'growth_ability'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    mbrg = CharField(32)
    nprg = CharField(32)
    nav = CharField(32)
    targ = CharField(32)
    epsg = CharField(32)
    seg = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class PayDebtAbility(BaseModel):
    """偿债能力"""
    class Meta:
        db_table = 'pay_debt_ability'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    currentratio = CharField(32)
    quickratio = CharField(32)
    cashratio = CharField(32)
    icratio = CharField(32)
    sheqratio = CharField(32)
    adratio = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class CashFlow(BaseModel):
    """现金流量"""
    class Meta:
        db_table = 'cash_flow'

    code = CharField(8)
    name = CharField(32)
    year = CharField(4)
    quarter = CharField(1)
    cf_sales = CharField(32)
    rateofreturn = CharField(32)
    cf_nm = CharField(32)
    cf_liabilities = CharField(32)
    cashflowratio = CharField(32)
    insert_date = DateField('%Y-%m-%d')


# #####################################################
# 宏观经济数据
# #####################################################
class DepositsRate(BaseModel):
    """存款利率"""
    class Meta:
        db_table = 'deposits_rate'

    date = DateField('%Y-%m-%d')
    deposit_type = CharField(32)
    rate = CharField(32)


class LoanRate(BaseModel):
    """贷款利率"""
    class Meta:
        db_table = 'loan_rate'

    date = DateField('%Y-%m-%d')
    loan_type = CharField(32)
    rate = CharField(32)


class RequiredReservesRate(BaseModel):
    """存款准备金率"""
    class Meta:
        db_table = 'required_reserves_rate'

    date = DateField('%Y-%m-%d')
    before = CharField(32)
    now = CharField(32)
    changed = CharField(32)


class MoneySupply(BaseModel):
    """货币供应量"""
    class Meta:
        db_table = 'money_supply'

    month = CharField(32)
    m2 = CharField(32)
    m2_yoy = CharField(32)
    m1 = CharField(32)
    m1_yoy = CharField(32)
    m0 = CharField(32)
    m0_yoy = CharField(32)
    cd = CharField(32)
    cd_yoy = CharField(32)
    qm = CharField(32)
    qm_yoy = CharField(32)
    ftd = CharField(32)
    ftd_yoy = CharField(32)
    sd = CharField(32)
    sd_yoy = CharField(32)
    rests = CharField(32)
    rests_yoy = CharField(32)


class MoneySupplyBal(BaseModel):
    """货币供应量(年底余额)"""
    class Meta:
        db_table = 'money_supply_bal'

    year = CharField(32)
    m2 = CharField(32)
    m1 = CharField(32)
    m0 = CharField(32)
    cd = CharField(32)
    qm = CharField(32)
    ftd = CharField(32)
    sd = CharField(32)
    rests = CharField(32)


class GrossDomesticProductYear(BaseModel):
    """国内生产总值(年度)"""
    class Meta:
        db_table = 'gdp_year'

    year = CharField(32)
    gdp = CharField(32)
    pc_gdp = CharField(32)
    gnp = CharField(32)
    pi = CharField(32)
    si = CharField(32)
    industry = CharField(32)
    cons_industry = CharField(32)
    ti = CharField(32)
    trans_industry = CharField(32)
    lbdy = CharField(32)


class GrossDomesticProductQuarter(BaseModel):
    """国内生产总值(季度)"""
    class Meta:
        db_table = 'gdp_quarter'

    quarter = CharField(32)
    gdp = CharField(32)
    gdp_yoy = CharField(32)
    pi = CharField(32)
    pi_yoy = CharField(32)
    si = CharField(32)
    si_yoy = CharField(32)
    ti = CharField(32)
    ti_yoy = CharField(32)


class GdpThreeDemands(BaseModel):
    """三大需求对GDP贡献"""
    class Meta:
        db_table = 'gdp_three_demands'

    year = CharField(32)
    end_for = CharField(32)
    for_rate = CharField(32)
    asset_for = CharField(32)
    asset_rate = CharField(32)
    goods_for = CharField(32)
    goods_rate = CharField(32)


class GdpThreeIndustryPull(BaseModel):
    """三大产业对GDP拉动"""
    class Meta:
        db_table = 'gdp_three_industry_pull'

    year = CharField(32)
    gdp_yoy = CharField(32)
    pi = CharField(32)
    si = CharField(32)
    industry = CharField(32)
    ti = CharField(32)


class GdpThreeIndustryContrib(BaseModel):
    """三大产业贡献率"""
    class Meta:
        db_table = 'gdp_three_industry_contrib'

    year = CharField(32)
    gdp_yoy = CharField(32)
    pi = CharField(32)
    si = CharField(32)
    industry = CharField(32)
    ti = CharField(32)


class CPI(BaseModel):
    """居民消费价格指数"""
    class Meta:
        db_table = 'cpi'

    month = CharField(32)
    cpi = CharField(32)


class PPI(BaseModel):
    """工业品出厂价格指数"""
    class Meta:
        db_table = 'ppi'

    month = CharField(32)
    ppiip = CharField(32)
    ppi = CharField(32)
    qm = CharField(32)
    rmi = CharField(32)
    pi = CharField(32)
    cg = CharField(32)
    food = CharField(32)
    clothing = CharField(32)
    roeu = CharField(32)
    dcg = CharField(32)


# #####################################################
# 龙虎榜数据
# #####################################################
class TopList(BaseModel):
    """每日龙虎榜列表"""
    class Meta:
        db_table = 'top_list'

    code = CharField(8)
    name = CharField(32)
    pchange = CharField(32)
    amount = CharField(32)
    buy = CharField(32)
    bratio = CharField(32)
    sell = CharField(32)
    sratio = CharField(32)
    reason = CharField(32)
    date = DateField('%Y-%m-%d')


class IndividualStatisticsTops(BaseModel):
    """个股上榜统计"""
    class Meta:
        db_table = 'individual_statistics_tops'

    code = CharField(8)
    name = CharField(32)
    days_type = CharField(3)
    count = CharField(32)
    bamount = CharField(32)
    samount = CharField(32)
    net = CharField(32)
    bcount = CharField(32)
    scount = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class BrokerTops(BaseModel):
    """营业部上榜统计"""
    class Meta:
        db_table = 'broker_tops'

    broker = CharField(32)
    days_type = CharField(3)
    count = CharField(32)
    bamount = CharField(32)
    bcount = CharField(32)
    samount = CharField(32)
    scount = CharField(32)
    top3 = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class InstitutionTops(BaseModel):
    """机构席位追踪"""
    class Meta:
        db_table = 'institution_tops'

    code = CharField(8)
    name = CharField(32)
    days_type = CharField(3)
    bamount = CharField(32)
    bcount = CharField(32)
    samount = CharField(32)
    scount = CharField(32)
    net = CharField(32)
    insert_date = DateField('%Y-%m-%d')


class InstitutionDetail(BaseModel):
    """机构成交明细"""
    class Meta:
        db_table = 'institution_detail'

    code = CharField(8)
    name = CharField(32)
    deal_date = DateField('%Y-%m-%d')
    bamount = CharField(32)
    samount = CharField(32)
    type = CharField(32)
    insert_date = DateField('%Y-%m-%d')


# #####################################################
# 银行间同业拆放利率
# #####################################################
class ShiborRate(BaseModel):
    """上海银行间同业拆放利率（Shanghai Interbank Offered Rate，简称Shibor）"""
    class Meta:
        db_table = 'shibor_rate'

    year = DateField('%Y')    # 指出是哪一年, 用于快速删除一整年数据
    date = DateField('%Y-%m-%d')
    ON = CharField(32)
    W1 = CharField(32)
    W2 = CharField(32)
    M1 = CharField(32)
    M3 = CharField(32)
    M6 = CharField(32)
    M9 = CharField(32)
    Y1 = CharField(32)


class ShiborQuote(BaseModel):
    """银行报价数据"""
    class Meta:
        db_table = 'shibor_quote'

    year = DateField('%Y')
    date = DateField('%Y-%m-%d')
    bank = CharField(32)
    ON = CharField(32)
    ON_B = CharField(32)
    ON_A = CharField(32)
    W1_B = CharField(32)
    W1_A = CharField(32)
    W2_B = CharField(32)
    W2_A = CharField(32)
    M1_B = CharField(32)
    M1_A = CharField(32)
    M3_B = CharField(32)
    M3_A = CharField(32)
    M6_B = CharField(32)
    M6_A = CharField(32)
    M9_B = CharField(32)
    M9_A = CharField(32)
    Y1_B = CharField(32)
    Y1_A = CharField(32)


class ShiborMA(BaseModel):
    """Shibor均值数据"""
    class Meta:
        db_table = 'shibor_ma'

    year = DateField('%Y')
    date = DateField('%Y-%m-%d')
    on_5 = CharField(32)
    on_10 = CharField(32)
    on_20 = CharField(32)
    W1_5 = CharField(32)
    W1_10 = CharField(32)
    W1_20 = CharField(32)
    W2_5 = CharField(32)
    W2_10 = CharField(32)
    W2_20 = CharField(32)
    M1_5 = CharField(32)
    M1_10 = CharField(32)
    M1_20 = CharField(32)
    M3_5 = CharField(32)
    M3_10 = CharField(32)
    M3_20 = CharField(32)
    M6_5 = CharField(32)
    M6_10 = CharField(32)
    M6_20 = CharField(32)
    M9_5 = CharField(32)
    M9_10 = CharField(32)
    M9_20 = CharField(32)
    Y1_5 = CharField(32)
    Y1_10 = CharField(32)
    Y1_20 = CharField(32)


class LPR(BaseModel):
    """贷款基础利率（LPR）"""
    class Meta:
        db_table = 'lpr'

    year = DateField('%Y')
    date = DateField('%Y-%m-%d')
    Y1 = CharField(32)


class LprMA(BaseModel):
    """LPR均值数据"""
    class Meta:
        db_table = 'lpr_ma'

    year = DateField('%Y')
    date = DateField('%Y-%m-%d')
    Y1_5 = CharField(32)
    Y1_10 = CharField(32)
    Y1_20 = CharField(32)
