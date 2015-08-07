#!/bin/bash
export OUTDIR=/var/log/pcap
cd $OUTDIR
for file in `ls -1 *.pcap | head -n -1`; do
  aws s3 cp "$file" "s3://mnms4graphs/unprocessed/$file"
  if [ "$?" -eq "0" ]; then
    rm "$file"
  else
    mv "$file" "$file.bad"
    echo "$file could not be uploaded"
  fi
done
