#!/bin/bash
source ~/.bashrc
workon trading
nohup python3 -u ../trading/scheduler/collectScheduler.py > out.log 2>&1 &