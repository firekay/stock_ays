#!/bin/bash
# run at 15:10

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

source ~/.zshenv
###################################################
# macro  宏观经济数据
##################################################
echo "$(date +'%Y%m%d %T'), begin run ${0} file" >> ${base_log_dir}/launchcrl_run.log 2>&1
python ${project_path}/main.py m -r > ${base_log_dir}/macro/save_required_reserves_rate.log 2>&1
python ${project_path}/main.py m -ms > ${base_log_dir}/macro/save_money_supply.log 2>&1
python ${project_path}/main.py m -msb > ${base_log_dir}/macro/save_money_supply_bal.log 2>&1
python ${project_path}/main.py m -gy > ${base_log_dir}/macro/save_gdp_year.log 2>&1
python ${project_path}/main.py m -gq > ${base_log_dir}/macro/save_gdp_quarter.log 2>&1
python ${project_path}/main.py m -gd > ${base_log_dir}/macro/save_gdp_three_demands.log 2>&1
python ${project_path}/main.py m -gip > ${base_log_dir}/macro/save_gdp_three_industry_pull.log 2>&1
python ${project_path}/main.py m -gic > ${base_log_dir}/macro/save_gdp_three_industry_contrib.log 2>&1
python ${project_path}/main.py m -c > ${base_log_dir}/macro/save_cpi.log 2>&1
python ${project_path}/main.py m -p > ${base_log_dir}/macro/save_ppi.log 2>&1

