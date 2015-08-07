#!/bin/bash


#MILLION_BYTES=10  #  Works out to be 10 MILLION_BYTES per file
SNAPLEN=150
OUTDIR=/var/log/pcap
IP=`hostname -I`
HOST=`grep $IP /etc/hosts | awk '{print $NF}'`
mkdir -p $OUTDIR/

tcpdump -Z root -G 120 -w "${OUTDIR}/traffic.${HOST}.%FT%T%z.pcap" -s $SNAPLEN \
'ip or icmp or tcp or udp' and not net 130.20.0.0/16 and not net 10.0.0.0/24 \
and not host 169.254.169.254 and not net 54.231.160.0/19 \
and not net 54.240.248.0/21
