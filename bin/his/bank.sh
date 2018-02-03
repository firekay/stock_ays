#!/bin/bash
# run at 16:10

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
source ~/.zshenv
cd ${project_path}

##################################################
# bank loan   银行间同业拆放利率
##################################################
echo "$(date +'%Y%m%d %T'), begin run ${0} file" >> ${base_log_dir}/launchcrl_run.log 2>&1
nohup python main.py l -r > ${base_log_dir}/bank/save_shibor_rate.log 2>&1
nohup python ${project_path}/main.py l -q > ${base_log_dir}/bank/save_shibor_quote.log 2>&1
nohup python ${project_path}/main.py l -m > ${base_log_dir}/bank/save_shibor_ma.log 2>&1
nohup python ${project_path}/main.py l -l > ${base_log_dir}/bank/save_lpr.log 2>&1
nohup python ${project_path}/main.py l -lm > ${base_log_dir}/bank/save_lpr_ma.log 2>&1
