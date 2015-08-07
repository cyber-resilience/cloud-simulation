#!/usr/bin/env python

import matplotlib.pyplot as plt
import sys
import math
import numpy as np

#determines the number of occurences of each distinct value in a given list
def freq_dist(lst, sz):
	freq = []
	for i in range(sz):
		freq.append(1)
	j = 0
	k = 0
	while(k < sz):
		while((j+1) < len(lst) and lst[j] == lst[j+1]):
			freq[k] = freq[k] + 1
			j = j + 1
		j = j + 1
		k = k + 1
	return freq

#takes the log of each value in a given list and returns the list of these values
def take_log(lst):
	n = []
	for i in range(len(lst)):
		if lst[i] == 0:
			n.append(0)
			continue
		n.append(math.log(lst[i]))
	return n

#read input files and store file names to a list
p_pagerank_file_list = open(sys.argv[1], 'r')
p_pagerank_files = in_file_list.readlines()
p_pagerank_file_list.close()
f_pagerank_file_list = open(sys.argv[4], 'r')
f_pagerank_files = f_in_file_list.readlines()
f_pagerank_file_list.close()

#process run for each file
q = 0
for x in range(len(f_pagerank_files)):
	#initialize lists to store node and degree information
	nodes = []
	pagerank = []
	c = 0
	while c < 4:
		#open the file containing the node and degree information
		F = open(str.strip(p_pagerank_files[q+c]), 'r')
		#read in each line and store value to appropriate lists
		for line in F:
			tmp = line.split()
			nodes.append(int(tmp[0]))
			pagerank.append(int(tmp[1]))
		F.close()
		c = c + 1
	#open the file containing the node and degree information
	F = open(str.strip(f_in_files[x]), 'r')
	#initialize lists to store node and degree information
	f_nodes = []
	f_pagerank = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		f_nodes.append(int(tmp[0]))
		f_pagerank.append(int(tmp[1]))
	F.close()
	if (x % 5) == 1:
		q = q + 4
	#sort each list so that instances of the same value will be adjacent to each other
	pagerank.sort()
	f_pagerank.sort()
	#convert list to a set to remove duplicates
	input_pagerank = list(set(pagerank))
	input_pagerank.sort()
	input_f_pagerank = list(set(f_pagerank))
	input_f_pagerank.sort()
	#determine number of different values for which frequency will be computed
	pfsize = len(input_pagerank)
	f_pfsize = len(input_f_pagerank)
	#compute the frequency of each value in the list and store the results in a new list
	freq_pagerank = freq_dist(pagerank, pfsize)
	freq_f_pagerank = freq_dist(f_pagerank, f_pfsize)
	#determine difference between Forest Fire values and originals
	#make master degree list for each degree type
	t = []
	for i in input_f_pagerank:
		t.append(i)
	for i in input_pagerank:
		t.append(i)
	pagerankMaster = list(set(t))
	pagerankMaster.sort()
	#fix frequency lists to included zeros for values in the master list but not the original for comparison purposes
	j = 0
	i = 0
	new_freq_pagerank = []
	for i in range(len(pagerankMaster)):
		if i >= len(input_pagerank):
			new_freq_pagerank.append(0)
			continue
		if pagerankMaster[i] == input_pagerank[j]:
			new_freq_pagerank.append(freq_pagerank[j])
			j = j + 1
			continue
		else:
			new_freq_pagerank.append(0)
	j = 0
	i = 0
	new_freq_f_pagerank = []
	for i in range(len(pagerankMaster)):
		if i >= len(input_f_pagerank):
			new_freq_f_pagerank.append(0)
			continue
		if pagerankMaster[i] == input_f_pagerank[j]:
			new_freq_f_pagerank.append(freq_f_pagerank[j])
			j = j + 1
		else:
			new_freq_f_pagerank.append(0)
	#calculate differences between frequencies for each degree value
	pagerankdiff = []
	k = 0
	for k in range(len(pagerankMaster)):
		pagerankdiff.append(abs(new_freq_f_pagerank[k] - new_freq_pagerank[k]))
	log_freq_pagerank = take_log(freq_pagerank)
	log_f_pagerank = take_log(input_f_pagerank)
	log_pagerank = take_log(input_pagerank)
	log_freq_f_pagerank = take_log(freq_f_pagerank)
	#plot results
	fig = plt.figure(figsize=(8,16))
	fig.suptitle(f_pagerank_files[x][29:(len(f_pagerank_files[x])-26)])
	idg = fig.add_subplot(211)
	idg.set_xlabel('Log Pagerank')
	idg.set_ylabel('Log Frequency')	
	idg.set_xscale('log')
	idg.set_yscale('log')
	idg.scatter(log_inDegree, log_freq_inDegree, s=20, c='b', marker='o', label='Original')
	idg.scatter(log_f_inDegree, log_freq_f_inDegree, s=20, c='r', marker='o', label='Forest Fire')
	idg.legend(loc='lower left')
	plt.xlim(0,10)
	d = fig.add_subplot(212)
	d.set_xlabel('Pagerank')
	d.set_ylabel('Frequency Difference')
	d.plot(inMaster, indiff, 'b', label='Pagerank')
	plt.xlim(0,20)
	d.legend(loc='best')
	fig.tight_layout()
	plt.savefig('ff_pagerank_{}.png'.format(f_pagerank_files[x][29:(len(f_pagerank_files[x])-26)]))
	

