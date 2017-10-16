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
year=$1

##################################################
# investment ref  投资参考数据
##################################################
python main.py -o i -d -y ${year} > ${base_log_dir}/investment/save_distribution_plans.log 2>&1 &
python main.py -o i -p -y ${year} > ${base_log_dir}/investment/save_performance_forecast.log 2>&1 &
python main.py -o i -r -y ${year} -m 1 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 2 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 3 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 4 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 5 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 6 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 7 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 8 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 9 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 10 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 11 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -r -y ${year} -m 12 >> ${base_log_dir}/investment/save_restricted_stock.log 2>&1 &
python main.py -o i -fh -y ${year} > ${base_log_dir}/investment/save_fund_holdings.log 2>&1 &
