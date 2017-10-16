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
#echo ${base_log_dir}
#echo ${project_path}
#echo ${project_path}/main.py
#echo ${daily_dir}
#echo $(pwd)
#exit

##################################################
# base  基本面数据
##################################################
python main.py -o b -pr -y ${year} > ${base_log_dir}/base/save_performance_report.log 2>&1 &
python main.py -o b -pa -y ${year} > ${base_log_dir}/base/save_profit_ability.log 2>&1 &
python main.py -o b -oa -y ${year} > ${base_log_dir}/base/save_operation_ability.log 2>&1 &
python main.py -o b -ga -y ${year} > ${base_log_dir}/base/save_growth_ability.log 2>&1 &
python main.py -o b -pd -y ${year} > ${base_log_dir}/base/save_pay_debt_ability.log 2>&1 &
python main.py -o b -c  -y ${year} > ${base_log_dir}/base/save_cash_flow.log 2>&1 &

