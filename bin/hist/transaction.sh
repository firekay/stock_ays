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

start=$1
end=$2

python main.py -o t -tk -d ${start} >> ${base_log_dir}/transaction/save_tick_data.log 2>&1 &
#
# python main.py -o t -bt -d ${start} > ${base_log_dir}/transaction/save_big_trade_data.log 2>&1 &
##python main.py -o t -btr -s ${start} -e ${end} > ${base_log_dir}/transaction/save_today_stocks_history_data.log 2>&1 &
