#!/bin/bash
# Downloads, Merges and Processes PCAP files with flower
# This file assumes it is run on a 2 minute schedule
export LD_LIBRARY_PATH=/usr/local/boost_1_58_0_shared64_release_multi/lib/:$LD_LIBRARY_PATH
BUCKET="mnms4graphs"
PREFIX="unprocessed"
S3LOC="s3://$BUCKET/$PREFIX"

PCAP_RAW="$HOME/$PREFIX"
PCAP_10_KEEP="$HOME/ten-min.pcap"
PCAP_10_TMP="$HOME/ten-min.pcap.tmp"
PCAP_2="$HOME/two-min.pcap"
PCAP_2_TMP="$HOME/two-min.pcap.tmp"

FLOWER_CONF="$HOME/flower.conf"
FLOWER_2="$HOME/flower-2"
FLOWER_10="$HOME/flower-10"

echo "INFO: Executing at `date`"
# Download PCAP files from S3
mkdir -p $PCAP_RAW/
aws s3 sync "$S3LOC/" $PCAP_RAW/
COUNT=`ls -1 $PCAP_RAW/*.pcap | wc -l`
if [ -z $COUNT ]; then
  echo "WARNING: No Files in S3"
  exit 1
fi

# Merge PCAP files from unprocessed
touch $PCAP_10_KEEP
if [ -s $PCAP_10_KEEP ]; then
  /usr/sbin/mergecap $PCAP_RAW/*.pcap $PCAP_10_KEEP -w $PCAP_10_TMP
else
  /usr/sbin/mergecap $PCAP_RAW/*.pcap -w $PCAP_10_TMP
fi
TEN_MINS_AGO=`date -d '-10 minutes' '+%F %T'`
TWO_MINS_AGO=`date -d ' -2 minutes' '+%F %T'`
echo editcap -A "$TEN_MINS_AGO" $PCAP_10_TMP $PCAP_10_KEEP
#/usr/sbin/editcap -A "$TEN_MINS_AGO" -B "$TWO_MINS_AGO" $PCAP_10_TMP $PCAP_10_KEEP
/usr/sbin/editcap -A "$TEN_MINS_AGO" $PCAP_10_TMP $PCAP_10_KEEP
rm -f $PCAP_2
rm -f $PCAP_2_TMP
/usr/sbin/mergecap $PCAP_RAW/*.pcap -w $PCAP_2
#/usr/sbin/mergecap $PCAP_RAW/*.pcap -w $PCAP_2_TMP
#/usr/sbin/editcap -A "$TWO_MINS_AGO" $PCAP_2_TMP $PCAP_2

# Execute Flower
mkdir -p $FLOWER_2
mkdir -p $FLOWER_10
rm -f $FLOWER_2/*.dat
rm -f $FLOWER_10/*.dat
/downloads/flower --config-file=$FLOWER_CONF --output-data-dir=$FLOWER_2 -s mnm $PCAP_2 2>/dev/null
/downloads/flower --config-file=$FLOWER_CONF --output-data-dir=$FLOWER_10 -s mnm $PCAP_10_KEEP 2>/dev/null
#aws s3 sync $FLOWER_2 "s3://$BUCKET/flower/2"
#aws s3 sync $FLOWER_10 "s3://$BUCKET/flower/10"

cat $FLOWER_2/*.dat  | grep ^1 | awk -F',' -v OFS=',' '{print $3,$4,$7,$8,$11,$12,$15,$16,$19,$20}' > $HOME/2_min.out
cat $FLOWER_10/*.dat | grep ^1 | awk -F',' -v OFS=',' '{print $3,$4,$7,$8,$11,$12,$15,$16,$19,$20}' > $HOME/10_min.out

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
rm -f $rmstr

USER=ec2-user
LOGNAME=ec2-user
HOME=/home/ec2-user
LANG=en_US.UTF-8
cd /home/ec2-user/mnm4graphs/demo_code
cp $HOME/*.out .
echo "INFO: STARTING MATLAB `date`"
/usr/local/bin/matlab -nodisplay -nodesktop -r "run Main_demo.m" | tail -5 | head -4 | ./create_html.pl > status.html
echo "INFO: MATLAB DONE `date`"
aws s3 cp latency_window.png s3://mnms4graphs/data/latency_window.png 
aws s3 cp status.html s3://mnms4graphs/data/status.html

exit 0
