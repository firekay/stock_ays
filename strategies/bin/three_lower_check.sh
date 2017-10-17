#!/usr/bin/env bash

bin_dir=$(echo $(cd $(dirname $0); pwd))
cd ${bin_dir}/..
mkdir -p logs

python three_lower_check.py -d 2017-10-13 > logs/three_lower_check_close.log 2>&1 &
