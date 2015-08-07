#!/bin/bash

#Input arguments are the name of the file to be processed (without the .tsv extension) and the lower and upper bounds for k.

GRAPH_DIRECTORY=~/kcore_tsv_files #Directory that holds the graph to be processed
KCORE_SUBDIRECTORY=kcore_graphs #Sub-directory to put the normalized results in

COUNTER=$2
UPPER=$3
let UPPER=UPPER+1
while [ $COUNTER -lt $UPPER ]; do
	./gen_kcore_graph.py $GRAPH_DIRECTORY/ $COUNTER #the directory here is the location of the .tsv files
#	vim $GRAPH_DIRECTORY/$KCORE_SUBDIRECTORY/kcore_$1.$COUNTER.csv -c '%s/,/ /g | wq' 
#	mv $GRAPH_DIRECTORY/$KCORE_SUBDIRECTORY/kcore_$1.$COUNTER.csv $GRAPH_DIRECTORY/$KCORE_SUBDIRECTORY/kcore_$1.$COUNTER.tsv
	let COUNTER=COUNTER+1
done

./normalize_tsv.py $GRAPH_DIRECTORY/$KCORE_SUBDIRECTORY

COUNTER=$2
while [ $COUNTER -lt $UPPER ]; do
	rm $GRAPH_DIRECTORY/$KCORE_SUBDIRECTORY/kcore_$1.$COUNTER.tsv
	let COUNTER=COUNTER+1
done
