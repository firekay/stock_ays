#!/bin/bash

ym=$(date +%Y%m)
day=$(date +%d)
daily_dir=$(echo $(cd $(dirname $0); pwd))
cd ${daily_dir}/../..
project_path=$(pwd)
logs_dir=${project_path}/logs/console
mkdir -p ${logs_dir}
cd ${daily_dir}
echo $(date +"%Y%m%d %T")', begin download base data.'
sh ${daily_dir}/base.sh
echo $(date +"%Y%m%d %T")', begin download bank data.'
sh ${padaily_dirth}/bank.sh
echo $(date +"%Y%m%d %T")', begin download classified data.'
sh ${daily_dir}/classified.sh
echo $(date +"%Y%m%d %T")', begin download investment ref data.'
sh ${daily_dir}/investment.sh
echo $(date +"%Y%m%d %T")', begin download transaction data.'
sh ${daily_dir}/transaction.sh
echo $(date +"%Y%m%d %T")', begin download winners data.'
sh ${daily_dir}/winners.sh

# 可一周调用一次
echo $(date +"%Y%m%d %T")', begin download macro data.'
sh ${daily_dir}/macro.sh
