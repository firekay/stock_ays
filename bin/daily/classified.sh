#!/bin/bash
# run at 15:30

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

###################################################
## classified  股票分类数据
###################################################
echo "$(date +'%Y%m%d %T'), begin run ${0} file" >> ${base_log_dir}/launchcrl_run.log 2>&1
python ${project_path}/main.py c -i > ${base_log_dir}/classified/save_industry_classified.log 2>&1
python ${project_path}/main.py c -c > ${base_log_dir}/classified/save_concept_classified.log 2>&1
python ${project_path}/main.py c -a > ${base_log_dir}/classified/save_area_classified.log 2>&1
python ${project_path}/main.py c -s > ${base_log_dir}/classified/save_sme_classified.log 2>&1
python ${project_path}/main.py c -g > ${base_log_dir}/classified/save_gem_classified.log 2>&1
python ${project_path}/main.py c -st > ${base_log_dir}/classified/save_st_classified.log 2>&1
python ${project_path}/main.py c -hs > ${base_log_dir}/classified/save_hs300s.log 2>&1
python ${project_path}/main.py c -sz > ${base_log_dir}/classified/save_sz50s.log 2>&1
python ${project_path}/main.py c -zz > ${base_log_dir}/classified/save_zz500s.log 2>&1
python ${project_path}/main.py c -t > ${base_log_dir}/classified/save_terminated.log 2>&1
python ${project_path}/main.py c -sp > ${base_log_dir}/classified/save_suspend.log 2>&1
