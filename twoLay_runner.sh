#!/bin/bash

#set environment
source /usr/share/modules/init/bash
module use -a /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate tf2_9

#run code
echo "Executing twoLay runner on" `hostname` "in $PWD"
/swbuild/analytix/tools/miniconda3_220407/envs/tf2_9/bin/python twoLay_runner.py $1