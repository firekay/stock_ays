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

###################################################
## winners  龙虎榜数据
###################################################
python main.py w -t -d ${today_line} > ${base_log_dir}/winners/save_top_list.log 2>&1 &
python main.py w -is > ${base_log_dir}/winners/save_individual_statistics_tops.log 2>&1 &
python main.py w -b > ${base_log_dir}/winners/save_broker_tops.log 2>&1 &
python main.py w -it > ${base_log_dir}/winners/save_institution_tops.log 2>&1 &
python main.py w -id > ${base_log_dir}/winners/save_institution_detail.log 2>&1 &

