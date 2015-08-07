#!/bin/bash


NUM_PKTS=1000000
BYTES=150
OUTDIR=/var/log
IP=`uname -n | sed -e "s/-/./g" | sed -e "s/^ip.//"`
HOST=`grep $IP /etc/hosts | awk '{print $NF}'`
index=0


while [ 1 ] 
do
  tcpdump -c $NUM_PKTS -w ${OUTDIR}/traffic.${HOST}.${index}.pcap -s $BYTES 'ip or icmp or tcp or udp' and  not net 130.20.0.0 mask 255.255.0.0 and not net 10.0.0.0 mask 255.255.255.0
  index=$((index + 1))
done
