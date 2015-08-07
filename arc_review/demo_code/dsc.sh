#!/bin/bash
USER=ec2-user
LOGNAME=ec2-user
HOME=/home/ec2-user
LANG=en_US.UTF-8
cd /home/ec2-user/mnm4graphs/demo_code
cp $HOME/*.out .
matlab -nodisplay -nodesktop -r "run Main_demo.m"
aws s3 cp latency_window.png s3://mnms4graphs/data/latency_window.png
