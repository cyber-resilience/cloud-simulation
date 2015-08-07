#!/bin/bash
MAX_TIME=120
count=6000
while [ `ping -c 1 172.31.2.53 | grep -c '1 received'` -gt 0 ]
do
  echo "Attacking $count times"
  SSH="ssh -i $HOME/mm.pem 172.31.2.53 timeout $MAX_TIME /data/bin/attack_web.sh $count"
  RAW=`/usr/bin/time -f '%e' /bin/bash -c "$SSH > $HOME/attack.out 2>&1" 2>&1 | awk -F'.' '{print $1}'`
done
