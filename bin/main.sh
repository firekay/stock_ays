#!/bin/bash

base_path=$(echo $(dirname $(pwd)))
today=$(date +%Y%m%d)
today_line=$(date +%Y-%m-%d)
yesterday_line=$(date -v -1d +%Y-%m-%d)
one_year_ago=$(date -v -1y +%Y-%m-%d)
ym=$(date +%Y%m)
day=$(date +%d)
base_log_dir=${base_path}/logs/${ym}/${day}
mkdir -p ${base_log_dir}
cd ${base_path}
python main.py > console$(date +%Y%m%d) 2>&1

##################################################
#  transaction  交易数据
##################################################
python main.py t -hk > ${base_log_dir}/save_stocks_k_data 2>&1 &
python main.py t -hky > ${base_log_dir}/save_yesterday_stocks_k_data 2>&1 &
python main.py t -hkt > ${base_log_dir}/save_today_stocks_k_data 2>&1 &
python main.py t -hi > ${base_log_dir}/save_stocks_hist_data 2>&1 &
python main.py t -hiy > ${base_log_dir}/save_yesterday_stocks_history_data 2>&1 &
python main.py t -hit > ${base_log_dir}/save_today_stocks_history_data 2>&1 &
python main.py t -r > ${base_log_dir}/save_stocks_revote_hist_data 2>&1 &
python main.py t -tad > ${base_log_dir}/save_today_all_data 2>&1 &
#python main.py t -tk -d ${today_line} > ${base_log_dir}/save_tick_data 2>&1 &
python main.py t -tkr -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/save_tick_data_range 2>&1 &
python main.py t -ttk > ${base_log_dir}/save_today_tick_data 2>&1 &
python main.py t -ttkt > ${base_log_dir}/save_today_tick_data_while_trading 2>&1 &
python main.py t -bi > ${base_log_dir}/save_big_index_data 2>&1 &
python main.py t -bt > ${base_log_dir}/save_big_trade_data 2>&1 &
python main.py t -btr -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/save_today_stocks_history_data 2>&1 &


##################################################
# investment ref  投资参考数据
##################################################
python main.py i -d > ${base_log_dir}/ssave_distribution_plans 2>&1 &
python main.py i -p > ${base_log_dir}/save_performance_forecast 2>&1 &
python main.py i -r > ${base_log_dir}/save_restricted_stock 2>&1 &
python main.py i -fh > ${base_log_dir}/save_fund_holdings 2>&1 &
python main.py i -n > ${base_log_dir}/save_new_stocks 2>&1 &
python main.py i -fsh -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/save_financing_securities_sh 2>&1 &
python main.py i -fsdh -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/save_financing_securities_detail_sh 2>&1 &
python main.py i -fsz -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/save_financing_securities_sz 2>&1 &
python main.py i -fsdz -d ${today_line} > ${base_log_dir}/save_financing_securities_detail_sz 2>&1 &

##################################################
# classified  股票分类数据
##################################################

##################################################
# base  基本面数据
##################################################

##################################################
# macro  宏观经济数据
##################################################

##################################################
# winners  龙虎榜数据
##################################################

##################################################
# bank loan   银行间同业拆放利率
##################################################

python main.py > $(date +%Y%m%d) 2>&1



