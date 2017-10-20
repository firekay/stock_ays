#!/bin/bash
# run at 22:00

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

# 保证当天的stock basic 先运行完
##################################################
#  transaction  交易数据
##################################################
# k data today
source ~/.zshenv
file_name=$(echo $(basename $0))
echo "$(date +'%Y%m%d %T'), begin run ${0} file" >> ${base_log_dir}/launchcrl_run.log 2>&1
python main.py t -hk -s ${today_line} -e ${today_line} -t 5 > ${base_log_dir}/transaction/save_today_stocks_k_data5.log 2>&1
python main.py t -hk -s ${today_line} -e ${today_line} -t 15 > ${base_log_dir}/transaction/save_today_stocks_k_data15.log 2>&1
python main.py t -hk -s ${today_line} -e ${today_line} -t 30 > ${base_log_dir}/transaction/save_today_stocks_k_data30.log 2>&1
# wait until hkt 30 over
python main.py t -hk -s ${today_line} -e ${today_line} -t 60 > ${base_log_dir}/transaction/save_today_stocks_k_data60.log 2>&1

