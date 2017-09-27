#!/bin/bash

basepath=$(echo $(dirname $(pwd)))
cd $basepath
python main.py > console$(date +%Y%m%d) 2>&1
# 全部时间全部股票历史交易数据(hist) save_all_days_all_stocks_hist_data
python main.py -t-a-a-h-d > logs/console/save_all_days_all_stocks_hist_data$(date +%Y%m%d) 2>&1

# 全部时间选择的股票历史交易数据(hist) save_all_days_select_stocks_hist_data
python main.py -t-a-s-h-d > logs/console/save_all_days_select_stocks_hist_data$(date +%Y%m%d) 2>&1

# 当天的全部股票的交易数据(hist) save_today_all_stocks_hist_data
python main.py -t-a-s-h-d > logs/console/save_today_all_stocks_hist_data$(date +%Y%m%d) 2>&1

# 当天的选择的股票的交易数据save_today_select_stocks_hist_data
python main.py -t-t-s-h-d > logs/console/save_today_select_stocks_hist_data$(date +%Y%m%d) 2>&1

# 昨天的全部股票的交易数据(hist) save_yestoday_all_stocks_hist_data
python main.py -t-y-a-h-d > logs/console/save_yestoday_all_stocks_hist_data$(date +%Y%m%d) 2>&1

# 昨天的选择的股票的交易数据save_yestoday_select_stocks_hist_data
python main.py -t-y-s-h-d > logs/console/save_yestoday_select_stocks_hist_data$(date +%Y%m%d) 2>&1



python main.py > $(date +%Y%m%d) 2>&1



