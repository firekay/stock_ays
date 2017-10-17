#!/usr/bin/env bash

bin_dir=$(echo $(cd $(dirname $0); pwd))
cd ${bin_dir}/..
mkdir -p logs

python three_upper_check.py -d 2017-10-13 > logs/three_upper_check_close.log 2>&1 &