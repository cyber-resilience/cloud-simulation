#!/bin/bash
# Downloads, Merges and Processes PCAP files with flower
export LD_LIBRARY_PATH=/usr/local/boost_1_58_0_shared64_release_multi/lib/:$LD_LIBRARY_PATH
MAX_TIME=120

BUCKET="mnms4graphs"
PREFIX="unprocessed"
S3LOC="s3://$BUCKET/$PREFIX"

PCAP_RAW="$HOME/$PREFIX"
PCAP_MERGED="$HOME/merged.pcap"

FLOWER_CONF="$HOME/flower.conf"
FLOWER_OUT="$HOME/flower-attack-out"
ATTACK_OUT="$HOME/attack"

for count in {250..6250..250}
do
  cd $HOME
  echo "INFO: Attacking $count times"
  SSH="ssh -i $HOME/mm.pem 172.31.2.53 timeout $MAX_TIME /data/bin/attack_web.sh $count"
  RAW=`/usr/bin/time -f '%e' /bin/bash -c "$SSH > /dev/null 2>&1" 2>&1 | awk -F'.' '{print $1}'`
  if [ $RAW -lt $MAX_TIME ]; then
    echo "INFO: Sleeping $(($MAX_TIME-$RAW))"
    sleep $(($MAX_TIME-$RAW))
  fi
  echo "INFO: Attack Done, Sleeping 180"
  sleep 180

  echo "INFO: Processing PCAP at `date`"
  # Download PCAP files from S3
  mkdir -p $PCAP_RAW/
  aws s3 sync "$S3LOC/" $PCAP_RAW/
  COUNT=`ls -1 $PCAP_RAW/*.pcap | wc -l`
  if [ -z $COUNT ]; then
    echo "WARNING: No Files in S3"
  fi

  # Merge PCAP files from unprocessed
  /usr/sbin/mergecap $PCAP_RAW/*.pcap -w $PCAP_MERGED
  
  # Execute Flower
  mkdir -p $FLOWER_OUT
  rm -f $FLOWER_OUT/*.dat
  /downloads/flower --config-file=$FLOWER_CONF --output-data-dir=$FLOWER_OUT -s mnm $PCAP_MERGED 2>/dev/null
  
  mkdir -p $ATTACK_OUT
  cat $FLOWER_OUT/*.dat > $ATTACK_OUT/${count}_attack.dat
  cat $ATTACK_OUT/${count}_attack.dat >> $ATTACK_OUT/all_attack.dat
  #cat $FLOWER_OUT/*.dat | grep ^1 | awk -F',' -v OFS=',' '{print $3,$4,$7,$8,$11,$12,$15,$16,$19,$20}' > $HOME/10_min.out
  
  # Delete PCAP files
  cd $PCAP_RAW
  
  str='aws s3api delete-objects --bucket '$BUCKET' --delete '\''{"Objects": ['
  rmstr=''
  for file in `ls -1 *.pcap`; do
    str+=' { "Key": "'$PREFIX'/'$file'" },'
    rmstr+=" $file"
  done
  str=${str%?}
  str+='],"Quiet": true}'\'

  eval $str
  rm $rmstr

done

cat $ATTACK_OUT/all_attack.dat | grep ^1 | grep ',8888' | awk -F',' -v OFS=',' '{print $3,$4,$7,$8,$11,$12,$15,$16,$19,$20}' > $ATTACK_OUT/all_attack.out
