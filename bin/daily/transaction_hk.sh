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
echo "$(date +'%Y%m%d %T'), begin run ${0} file" > ${base_log_dir}/${file_name}.log 2>&1
python main.py t -hkt -t D > ${base_log_dir}/transaction/save_today_stocks_k_dataD.log 2>&1
python main.py t -hkt -t W > ${base_log_dir}/transaction/save_today_stocks_k_dataW.log 2>&1
python main.py t -hkt -t M > ${base_log_dir}/transaction/save_today_stocks_k_dataM.log 2>&1
# wait until hkt 30 over
python main.py t -hkt -t 60 > ${base_log_dir}/transaction/save_today_stocks_k_data60.log 2>&1

# hist data today
python main.py t -hit -t D > ${base_log_dir}/transaction/save_today_stocks_history_dataD.log 2>&1
python main.py t -hit -t W > ${base_log_dir}/transaction/save_today_stocks_history_dataW.log 2>&1
python main.py t -hit -t M > ${base_log_dir}/transaction/save_today_stocks_history_dataM.log 2>&1
# wait util hit m over

#python main.py t -hit -t 5 > ${base_log_dir}/transaction/save_today_stocks_history_data.log 2>&1 &
#python main.py t -hit -t 15 > ${base_log_dir}/transaction/save_today_stocks_history_data.log 2>&1 &
#python main.py t -hit -t 30 > ${base_log_dir}/transaction/save_today_stocks_history_data.log 2>&1 &
#python main.py t -hit -t 60 > ${base_log_dir}/transaction/save_today_stocks_history_data.log 2>&1 &

python main.py t -r -s ${today_line} -e ${today_line} > ${base_log_dir}/transaction/save_stocks_revote_hist_data.log 2>&1
python main.py t -bi > ${base_log_dir}/transaction/save_big_index_data.log 2>&1
python main.py t -bt > ${base_log_dir}/transaction/save_big_trade_data.log 2>&1
python main.py t -tk -d ${today_line} > ${base_log_dir}/transaction/save_tick_data.log 2>&1
## use after 6pm clock, the same with 'python main.py t -tk -d ${today_line}'
##python main.py t -ttk > ${base_log_dir}/transaction/save_today_tick_data.log 2>&1 &
## use before 6pm clock
##python main.py t -ttkt > ${base_log_dir}/transaction/save_today_tick_data_while_trading.log 2>&1 &
#
##python main.py t -btr -s ${one_year_ago} -e ${today_line} > ${base_log_dir}/transaction/save_today_stocks_history_data.log 2>&1 &
