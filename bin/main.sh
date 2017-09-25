#!/bin/bash

basepath=$(echo $(dirname $(pwd)))
cd $basepath
python main.py > console$(date +%Y%m%d) 2>&1