#!/bin/bash

base_path=$(echo $(dirname $(pwd)))
today=$(date +%Y%m%d)
today_line=$(date +%Y-%m-%d)
yesterday_line=$(date -v -1d +%Y-%m-%d)
one_year_ago=$(date -v -1y +%Y-%m-%d)
ym=$(date +%Y%m)
day=$(date +%d)
base_log_dir=${base_path}/logs/${ym}/${day}
mkdir -p ${base_log_dir}/{transaction,investment,classified,base,macro,winners,bank}
cd ${base_path}


###################################################
## base  基本面数据
###################################################
#python main.py b -d ${yesterday_line} -s > ${base_log_dir}/base/save_stocks_basic_data_yesterday.log 2>&1
#python main.py b -pr > ${base_log_dir}/base/save_performance_report_yesterday.log 2>&1 &
#python main.py b -pa > ${base_log_dir}/base/save_profit_ability_yesterday.log 2>&1 &
#python main.py b -oa > ${base_log_dir}/base/save_operation_ability_yesterday.log 2>&1 &
#python main.py b -ga > ${base_log_dir}/base/save_growth_ability_yesterday.log 2>&1 &
#python main.py b -pd > ${base_log_dir}/base/save_pay_debt_ability_yesterday.log 2>&1 &
#python main.py b -c > ${base_log_dir}/base/save_cash_flow_yesterday.log 2>&1 &


##################################################
#  transaction  交易数据
##################################################
# k data yesterday
# python main.py t -hky -t D > ${base_log_dir}/transaction/save_stocks_k_dataD_yesterday.log 2>&1 &
 python main.py t -hky -t W > ${base_log_dir}/transaction/save_stocks_k_dataW_yesterday.log 2>&1 &
 python main.py t -hky -t M > ${base_log_dir}/transaction/save_stocks_k_dataM_yesterday.log 2>&1 &
# python main.py t -hky -t 5 > ${base_log_dir}/transaction/save_stocks_k_data5_yesterday.log 2>&1 &
# python main.py t -hky -t 15 > ${base_log_dir}/transaction/save_stocks_k_data15_yesterday.log 2>&1 &
# python main.py t -hky -t 30 > ${base_log_dir}/transaction/save_stocks_k_data30_yesterday.log 2>&1 &
# python main.py t -hky -t 60 > ${base_log_dir}/transaction/save_stocks_k_data60_yesterday.log 2>&1 &

#python main.py t -hiy -t D > ${base_log_dir}/transaction/save_stocks_history_dataD_yesterday.log 2>&1 &
python main.py t -hiy -t W > ${base_log_dir}/transaction/save_stocks_history_dataW_yesterday.log 2>&1 &
python main.py t -hiy -t M > ${base_log_dir}/transaction/save_stocks_history_dataM_yesterday.log 2>&1 &
#python main.py t -hiy -t 5 > ${base_log_dir}/transaction/save_stocks_history_data_yesterday.log 2>&1 &
#python main.py t -hiy -t 15 > ${base_log_dir}/transaction/save_stocks_history_data_yesterday.log 2>&1 &
#python main.py t -hiy -t 30 > ${base_log_dir}/transaction/save_stocks_history_data_yesterday.log 2>&1 &
#python main.py t -hiy -t 60 > ${base_log_dir}/transaction/save_stocks_history_data_yesterday.log 2>&1 &

#python main.py t -r -s ${today_line} -e ${today_line} > ${base_log_dir}/transaction/save_stocks_revote_hist_data_yesterday.log 2>&1 &
#python main.py t -tad > ${base_log_dir}/transaction/save_today_all_data_yesterday.log 2>&1 &
#python main.py t -tk -d ${yesterday_line} > ${base_log_dir}/transaction/save_tick_data_yesterday_yesterday.log 2>&1 &
#python main.py t -tkr -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/transaction/save_tick_data_range_yesterday.log 2>&1 &

# use after 6pm clock, the same with 'python main.py t -tk -d ${today_line}'
# use before 6pm clock
#python main.py t -ttkt > ${base_log_dir}/transaction/save_today_tick_data_while_trading_yesterday.log 2>&1 &

#python main.py t -bi > ${base_log_dir}/transaction/save_big_index_data_yesterday.log 2>&1 &
#python main.py t -bt > ${base_log_dir}/transaction/save_big_trade_data_yesterday.log 2>&1 &
#python main.py t -btr -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/transaction/save_today_stocks_history_data_yesterday.log 2>&1 &


###################################################
## investment ref  投资参考数据
###################################################
#python main.py i -d > ${base_log_dir}/investment/ssave_distribution_plans_yesterday.log 2>&1 &
#python main.py i -p > ${base_log_dir}/investment/save_performance_forecast_yesterday.log 2>&1 &
#python main.py i -r > ${base_log_dir}/investment/save_restricted_stock_yesterday.log 2>&1 &
#python main.py i -fh > ${base_log_dir}/investment/save_fund_holdings_yesterday.log 2>&1 &
#python main.py i -n > ${base_log_dir}/investment/save_new_stocks_yesterday.log 2>&1 &
#python main.py i -fsh -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_sh_yesterday.log 2>&1 &
#python main.py i -fsdh -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_detail_sh_yesterday.log 2>&1 &
#python main.py i -fsz -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_sz_yesterday.log 2>&1 &
#python main.py i -fsdz -d ${today_line} > ${base_log_dir}/investment/save_financing_securities_detail_sz_yesterday.log 2>&1 &

###################################################
## classified  股票分类数据
###################################################
#python main.py c -i > ${base_log_dir}/classified/save_industry_classified_yesterday.log 2>&1 &
#python main.py c -c > ${base_log_dir}/classified/save_concept_classified_yesterday.log 2>&1 &
#python main.py c -a > ${base_log_dir}/classified/save_area_classified_yesterday.log 2>&1 &
#python main.py c -s > ${base_log_dir}/classified/save_sme_classified_yesterday.log 2>&1 &
#python main.py c -g > ${base_log_dir}/classified/save_gem_classified_yesterday.log 2>&1 &
#python main.py c -st > ${base_log_dir}/classified/save_st_classified_yesterday.log 2>&1 &
#python main.py c -hs > ${base_log_dir}/classified/save_hs300s_yesterday.log 2>&1 &
#python main.py c -sz > ${base_log_dir}/classified/save_sz50s_yesterday.log 2>&1 &
#python main.py c -zz > ${base_log_dir}/classified/save_zz500s_yesterday.log 2>&1 &
#python main.py c -t > ${base_log_dir}/classified/save_terminated_yesterday.log 2>&1 &
#python main.py c -sp > ${base_log_dir}/classified/save_suspend_yesterday.log 2>&1 &

###################################################
## macro  宏观经济数据
###################################################
#python main.py m -r > ${base_log_dir}/macro/save_required_reserves_rate_yesterday.log 2>&1 &
#python main.py m -ms > ${base_log_dir}/macro/save_money_supply_yesterday.log 2>&1 &
#python main.py m -msb > ${base_log_dir}/macro/save_money_supply_bal_yesterday.log 2>&1 &
#python main.py m -gy > ${base_log_dir}/macro/save_gdp_year_yesterday.log 2>&1 &
#python main.py m -gq > ${base_log_dir}/macro/save_gdp_quarter_yesterday.log 2>&1 &
#python main.py m -gd > ${base_log_dir}/macro/save_gdp_three_demands_yesterday.log 2>&1 &
#python main.py m -gip > ${base_log_dir}/macro/save_gdp_three_industry_pull_yesterday.log 2>&1 &
#python main.py m -gic > ${base_log_dir}/macro/save_gdp_three_industry_contrib_yesterday.log 2>&1 &
#python main.py m -c > ${base_log_dir}/macro/save_cpi_yesterday.log 2>&1 &
#python main.py m -p > ${base_log_dir}/macro/save_ppi_yesterday.log 2>&1 &

###################################################
## winners  龙虎榜数据
###################################################
#python main.py w -t -d ${yesterday_line} > ${base_log_dir}/winners/save_top_list_yesterday.log 2>&1 &
#python main.py w -is > ${base_log_dir}/winners/save_individual_statistics_tops_yesterday.log 2>&1 &
#python main.py w -b > ${base_log_dir}/winners/save_broker_tops_yesterday.log 2>&1 &
#python main.py w -it > ${base_log_dir}/winners/save_institution_tops_yesterday.log 2>&1 &
#python main.py w -id > ${base_log_dir}/winners/save_institution_detail_yesterday.log 2>&1 &

###################################################
## bank loan   银行间同业拆放利率
###################################################
#python main.py l -r > ${base_log_dir}/bank/save_shibor_rate_yesterday.log 2>&1 &
#python main.py l -q > ${base_log_dir}/bank/save_shibor_quote_yesterday.log 2>&1 &
#python main.py l -m > ${base_log_dir}/bank/save_shibor_ma_yesterday.log 2>&1 &
#python main.py l -l > ${base_log_dir}/bank/save_lpr_yesterday.log 2>&1 &
#python main.py l -lm > ${base_log_dir}/bank/save_shibor_rate_yesterday.log 2>&1 &

