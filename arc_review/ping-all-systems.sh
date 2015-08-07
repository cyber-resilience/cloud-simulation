#!/bin/bash
IPS=`aws ec2 describe-instances --region=us-west-2 | grep PrivateIpAddress | grep 172 | awk '{print $NF}'| sed -e 's/"//g' | sed -e 's/,//g' | sort | uniq`
for ip in $IPS; do
  ping -c 1 $ip >/dev/null 2>&1 &
done
