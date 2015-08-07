#!/bin/bash
HOST=web1
FILE=`curl -XGET "http://$HOST:8888/get_filelist" 2> /dev/null | head -1`
a=$1
#while true; do
  echo "Attacking $a times, `date`"
  for b in `seq 1 $a`; do
    curl -XGET "http://$HOST:8888/get_file?name=$FILE" > /dev/null 2> /dev/null &
  done
  wait
  echo "Done, `date`"
#done
