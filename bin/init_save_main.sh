#!/usr/bin/env bash

base_path=$(echo $(dirname $(pwd)))
today=$(date +%Y%m%d)
today_line=$(date +%Y-%m-%d)
yesterday_line=$(date -v -1d +%Y-%m-%d)
one_month_ago=$(date -v -1m +%Y-%m-%d)
two_month_ago=$(date -v -2m +%Y-%m-%d)
one_year_ago=$(date -v -1y +%Y-%m-%d)
five_year_ago=$(date -v -5y +%Y-%m-%d)
ym=$(date +%Y%m)
day=$(date +%d)
base_log_dir=${base_path}/logs/${ym}/${day}
mkdir -p ${base_log_dir}/{transaction,investment,classified,base,macro,winners,bank}
cd ${base_path}

###################################################
##  transaction  交易数据
###################################################
python main.py t -hk > ${base_log_dir}/transaction/save_stocks_k_data.log 2>&1 &
python main.py t -hi > ${base_log_dir}/transaction/save_stocks_hist_data.log 2>&1 &
python main.py t -r > ${base_log_dir}/transaction/save_stocks_revote_hist_data.log 2>&1 &
python main.py t -tad > ${base_log_dir}/transaction/save_today_all_data.log 2>&1 &
#python main.py t -tkr -s ${one_month_ago} -e ${today_line} > ${base_log_dir}/transaction/save_tick_data_range.log 2>&1 &
#python main.py t -ttk > ${base_log_dir}/transaction/save_today_tick_data.log 2>&1 &
#python main.py t -ttkt > ${base_log_dir}/transaction/save_today_tick_data_while_trading.log 2>&1 &
python main.py t -bi > ${base_log_dir}/transaction/save_big_index_data.log 2>&1 &
python main.py t -btr -s ${one_month_ago} -e ${today_line} > ${base_log_dir}/transaction/save_big_trade_data_range.log 2>&1 &


###################################################
## investment ref  投资参考数据
###################################################
#python main.py i -d > ${base_log_dir}/investment/ssave_distribution_plans.log 2>&1 &
#python main.py i -p > ${base_log_dir}/investment/save_performance_forecast.log 2>&1 &
#python main.py i -r > ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
#python main.py i -fh > ${base_log_dir}/investment/save_fund_holdings.log 2>&1 &
#python main.py i -n > ${base_log_dir}/investment/save_new_stocks.log 2>&1 &
#python main.py i -fsh -s ${five_year_ago} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_sh.log 2>&1 &
#python main.py i -fsdh -s ${five_year_ago} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_detail_sh.log 2>&1 &
#python main.py i -fsz -s ${five_year_ago} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_sz.log 2>&1 &
#python main.py i -fsdz -d ${today_line} > ${base_log_dir}/investment/save_financing_securities_detail_sz.log 2>&1 &

###################################################
## classified  股票分类数据
###################################################
#python main.py c -i > ${base_log_dir}/classified/save_industry_classified.log 2>&1 &
#python main.py c -c > ${base_log_dir}/classified/save_concept_classified.log 2>&1 &
#python main.py c -a > ${base_log_dir}/classified/save_area_classified.log 2>&1 &
#python main.py c -s > ${base_log_dir}/classified/save_sme_classified.log 2>&1 &
#python main.py c -g > ${base_log_dir}/classified/save_gem_classified.log 2>&1 &
#python main.py c -st > ${base_log_dir}/classified/save_st_classified.log 2>&1 &
#python main.py c -hs > ${base_log_dir}/classified/save_hs300s.log 2>&1 &
#python main.py c -sz > ${base_log_dir}/classified/save_sz50s.log 2>&1 &
#python main.py c -zz > ${base_log_dir}/classified/save_zz500s.log 2>&1 &
#python main.py c -t > ${base_log_dir}/classified/save_terminated.log 2>&1 &
#python main.py c -sp > ${base_log_dir}/classified/save_suspend.log 2>&1 &

###################################################
## base  基本面数据
###################################################
#python main.py b -s > ${base_log_dir}/base/save_stocks_basic_data.log 2>&1 &
#python main.py b -pr > ${base_log_dir}/base/save_performance_report.log 2>&1 &
#python main.py b -pa > ${base_log_dir}/base/save_profit_ability.log 2>&1 &
#python main.py b -oa > ${base_log_dir}/base/save_operation_ability.log 2>&1 &
#python main.py b -ga > ${base_log_dir}/base/save_growth_ability.log 2>&1 &
#python main.py b -pd > ${base_log_dir}/base/save_pay_debt_ability.log 2>&1 &
#python main.py b -c > ${base_log_dir}/base/save_cash_flow.log 2>&1 &

###################################################
## macro  宏观经济数据
###################################################
#python main.py m -r > ${base_log_dir}/macro/save_required_reserves_rate.log 2>&1 &
#python main.py m -ms > ${base_log_dir}/macro/save_money_supply.log 2>&1 &
#python main.py m -msb > ${base_log_dir}/macro/save_money_supply_bal.log 2>&1 &
#python main.py m -gy > ${base_log_dir}/macro/save_gdp_year.log 2>&1 &
#python main.py m -gq > ${base_log_dir}/macro/save_gdp_quarter.log 2>&1 &
#python main.py m -gd > ${base_log_dir}/macro/save_gdp_three_demands.log 2>&1 &
#python main.py m -gip > ${base_log_dir}/macro/save_gdp_three_industry_pull.log 2>&1 &
#python main.py m -gic > ${base_log_dir}/macro/save_gdp_three_industry_contrib.log 2>&1 &
#python main.py m -c > ${base_log_dir}/macro/save_cpi.log 2>&1 &
#python main.py m -p > ${base_log_dir}/macro/save_ppi.log 2>&1 &

###################################################
## winners  龙虎榜数据
###################################################
#python main.py w -t -d ${today_line} > ${base_log_dir}/winners/save_top_list.log 2>&1 &
#python main.py w -is > ${base_log_dir}/winners/save_individual_statistics_tops.log 2>&1 &
#python main.py w -b > ${base_log_dir}/winners/save_broker_tops.log 2>&1 &
#python main.py w -it > ${base_log_dir}/winners/save_institution_tops.log 2>&1 &
#python main.py w -id > ${base_log_dir}/winners/save_institution_detail.log 2>&1 &

###################################################
## bank loan   银行间同业拆放利率
###################################################
#python main.py l -r > ${base_log_dir}/bank/save_shibor_rate.log 2>&1 &
#python main.py l -q > ${base_log_dir}/bank/save_shibor_quote.log 2>&1 &
#python main.py l -m > ${base_log_dir}/bank/save_shibor_ma.log 2>&1 &
#python main.py l -l > ${base_log_dir}/bank/save_lpr.log 2>&1 &
#python main.py l -lm > ${base_log_dir}/bank/save_shibor_rate.log 2>&1 &

