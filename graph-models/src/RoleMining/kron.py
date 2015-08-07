#!/usr/bin/env python

import os
import sys
import math

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
	n = math.log(len(nodes),2)
	print n
	kronfit = "~/share_folder/Snap-2.0/examples/kronfit/kronfit -i:{0} -o:{1}".format(files[x].strip(), files[x][19:(len(files[x])-5)])
	os.system(kronfit) 
	F = open('KronFit-{}.tab'.format(files[x][19:(len(files[x])-5)]), 'r')
	tmp = F.readlines()
	i = len(tmp) - 1
	start = tmp[i].find('[')
	end = tmp[i].find(']')
	init = tmp[i][(start+1):end]
	krongen = '~/share_folder/Snap-2.0/examples/krongen/krongen -o:{0}.txt -m:"{1}" -i:{2}'.format(files[x][19:(len(files[x])-5)], init, str(int(n)))
	os.system(krongen)
