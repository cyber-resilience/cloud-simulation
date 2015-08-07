#!/usr/bin/env python

import os
import sys
import math
import numpy as np

#read input file and store file names to a list
file_list = open(sys.argv[1], 'r')
files = file_list.readlines()
file_list.close()

for x in range(len(files)):
	f = open(files[x].strip(), 'r')
	nodes = []
	#convert node labels to integers so they can be sorted
	for line in f:
		tmp = line.split()
		for i in tmp:
			nodes.append(int(i))
	f.close()
	#remove duplicates from the list
	nodes = list(set(nodes))
	n = len(nodes)
	for y in np.arange(0.2, 0.5, 0.1):
		forestfire = "~/share_folder/Snap-2.0/examples/forestfire/forestfire -o:{0}_{1}_forestfire.txt -n:{2} -f:{3} -b:0.32".format(files[x][19:(len(files[x])-20)], str(y), str(n), str(y))
		os.system(forestfire)
