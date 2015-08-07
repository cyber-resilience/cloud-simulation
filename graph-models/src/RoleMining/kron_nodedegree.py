#!/usr/bin/env python

import matplotlib.pyplot as plt
import sys

## {{{ http://code.activestate.com/recipes/81188/ (r1)
def binary_search(seq, t):
    min = 0; max = len(seq) - 1
    while 1:
        if max < min:
	    return -1
        m = (min + max) / 2
        if seq[m] < t:
            min = m + 1
        elif seq[m] > t:
            max = m - 1
        else:	
            return m
## end of http://code.activestate.com/recipes/81188/ }}}


#read input file and store file names to a list
file_list = open(sys.argv[1], 'r')
files = file_list.readlines()
file_list.close()

#process is applied to each .tsv file
for x in files:
	f = open(str.strip(x), 'r')
	nodes = []
	#convert node labels to integers so they can be sorted
	for line in f:
		if line[0] == '#':
			continue
		tmp = line.split()
		for i in tmp:
			nodes.append(int(i))
	#remove duplicates from the list
	nodes = list(set(nodes))
	#sort the list
	nodes.sort()
	nodeCount = len(nodes)
	#initialize lists to store the in and out degrees for each node and fill with zeros
	inDegree = []
	outDegree = []
	for k in range(nodeCount):
		inDegree.append(0)
		outDegree.append(0)
	#for each edge listed, update the respective in degree and out degree for the nodes listed
	f.seek(0)
	for line in f:
		if line[0] == '#':
			continue
		t = line.split()
		tmp = []
		for l in t:
			tmp.append(int(l))	
		j = binary_search(nodes, tmp[0])
		outDegree[j] = outDegree[j] + 1
		k = binary_search(nodes, tmp[1])
		inDegree[k] = inDegree[k] + 1 
	f.close()
	degree = []
	for p in range(nodeCount):
		degree.append(inDegree[p] + outDegree[p])
	#print nodes 
	#print inDegree
	F = open('/home/ubuntu/KronCAIDAOutDegree/' + x[13:(len(x)-5)] + '_degree_out.txt', 'w')
	for m in range(nodeCount):
		s = str(nodes[m]) + '\t' + str(outDegree[m]) + '\n'
		F.write(s)
	F.close()
	F = open('/home/ubuntu/KronCAIDAInDegree/' + x[13:(len(x)-5)] + '_degree_in.txt', 'w')
	for n in range(nodeCount):
		s = str(nodes[n]) + '\t' + str(inDegree[n]) + '\n'
		F.write(s)
	F.close()
	F = open('/home/ubuntu/KronCAIDADegree/' + x[13:(len(x)-5)] + '_degree.txt', 'w')
	for q in range(nodeCount):
		s = str(nodes[q]) + '\t' + str(degree[q]) + '\n'
		F.write(s)
	F.close()
			 
