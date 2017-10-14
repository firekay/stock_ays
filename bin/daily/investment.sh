#!/bin/bash

today=$(date +%Y%m%d)
today_line=$(date +%Y-%m-%d)
yesterday_line=$(date -v -1d +%Y-%m-%d)
one_year_ago=$(date -v -1y +%Y-%m-%d)
ym=$(date +%Y%m)
day=$(date +%d)
daily_dir=$(echo $(cd $(dirname $0); pwd))
cd ${daily_dir}/../..
project_path=$(pwd)
base_log_dir=${project_path}/logs/${ym}/${day}
mkdir -p ${base_log_dir}/{transaction,investment,classified,base,macro,winners,bank}
cd ${project_path}

##################################################
# investment ref  投资参考数据
##################################################
python main.py i -d > ${base_log_dir}/investment/save_distribution_plans.log 2>&1 &
python main.py i -p > ${base_log_dir}/investment/save_performance_forecast.log 2>&1 &
python main.py i -r > ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py i -fh > ${base_log_dir}/investment/save_fund_holdings.log 2>&1 &
python main.py i -n > ${base_log_dir}/investment/save_new_stocks.log 2>&1 &
python main.py i -fsh -s ${today_line} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_sh.log 2>&1 &
python main.py i -fsdh --date ${today_line} > ${base_log_dir}/investment/save_financing_securities_detail_sh.log 2>&1 &
python main.py i -fsz -s ${today_line} -e ${today_line} > ${base_log_dir}/investment/save_financing_securities_sz.log 2>&1 &
python main.py i -fsdz --date ${today_line} > ${base_log_dir}/investment/save_financing_securities_detail_sz.log 2>&1 &
