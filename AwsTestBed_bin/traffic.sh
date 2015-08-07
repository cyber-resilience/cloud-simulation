#!/bin/bash


MILLION_BYTES=10  #  Works out to be 10 MILLION_BYTES per file
SNAPLEN=150
OUTDIR=/var/log
IP=`uname -n | sed -e "s/-/./g" | sed -e "s/^ip.//"`
HOST=`grep $IP /etc/hosts | awk '{print $NF}'`
index=0


tcpdump -C $MILLION_BYTES -w ${OUTDIR}/traffic.${HOST}.${index}.pcap -s $SNAPLEN 'ip or icmp or tcp or udp' and  not net 130.20.0.0 mask 255.255.0.0 and not net 10.0.0.0 mask 255.255.255.0
