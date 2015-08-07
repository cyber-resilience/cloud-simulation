#!/bin/bash

# REMOVE Files being generated too fast to be ingested
find /data/genfile -mmin +120 -type f -name "*.csv"  -exec rm -f {} \;

# REMOVE Files that have been ingested
find /data/genfile -mmin  +20 -type f -name "*.done" -exec rm -f {} \;

# REMOVE Files that have been retrieved
find /data/getfile -mmin +120 -type f -name "*.txt"  -exec rm -f {} \;

# REMOVE Files to reducing the amount of network traffic capture to the last hour
find /var/log      -mmin  +60 -type f -name "*.pcap" -exec rm -f {} \;
