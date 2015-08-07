#!/usr/bin/env python

import matplotlib.pyplot as plt
import math
import numpy as np
import sys

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
in_file_list = open(sys.argv[1], 'r')
in_files = in_file_list.readlines()
in_file_list.close()
out_file_list = open(sys.argv[2], 'r')
out_files = out_file_list.readlines()
out_file_list.close()
deg_file_list = open(sys.argv[3], 'r')
deg_files = deg_file_list.readlines()
deg_file_list.close()
f_in_file_list = open(sys.argv[4], 'r')
f_in_files = f_in_file_list.readlines()
f_in_file_list.close()
f_out_file_list = open(sys.argv[5], 'r')
f_out_files = f_out_file_list.readlines()
f_out_file_list.close()
f_deg_file_list = open(sys.argv[6], 'r')
f_deg_files = f_deg_file_list.readlines()
f_deg_file_list.close()

#process run for each file
q = 0
for x in range(len(f_in_files)):
	#open the file containing the node and degree information
	F = open(str.strip(in_files[q]), 'r')
	#initialize lists to store node and degree information
	nodes = []
	inDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		nodes.append(int(tmp[0]))
		inDegree.append(int(tmp[1]))
	F.close()
	#open the file containing the node and degree information
	F = open(str.strip(f_in_files[x]), 'r')
	#initialize lists to store node and degree information
	f_nodes = []
	f_inDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		f_nodes.append(int(tmp[0]))
		f_inDegree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(out_files[q]), 'r')
	#initialize lists to store node and degree information
	outDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		outDegree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(f_out_files[x]), 'r')
	#initialize lists to store node and degree information
	f_outDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		f_outDegree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(deg_files[q]), 'r')
	#initialize lists to store node and degree information
	degree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		degree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(f_deg_files[x]), 'r')
	#initialize lists to store node and degree information
	f_degree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		f_degree.append(int(tmp[1]))
	F.close()
	if (x % 2) == 1:
		q = q + 1
	#sort each list so that instances of the same value will be adjacent to each other
	inDegree.sort()
	f_inDegree.sort()
	#convert list to a set to remove duplicates
	input_inDegree = list(set(inDegree))
	input_inDegree.sort()
	input_f_inDegree = list(set(f_inDegree))
	input_f_inDegree.sort()
	#determine number of different values for which frequency will be computed
	ifsize = len(input_inDegree)
	f_ifsize = len(input_f_inDegree)
	#compute the frequency of each value in the list and store the results in a new list
	freq_inDegree = freq_dist(inDegree, ifsize)
	freq_f_inDegree = freq_dist(f_inDegree, f_ifsize)
	#repeat above for remaining lists
	outDegree.sort()
	input_outDegree = list(set(outDegree))
	input_outDegree.sort()
	ofsize = len(input_outDegree)
	freq_outDegree = freq_dist(outDegree, ofsize)
	degree.sort()
	input_degree = list(set(degree))
	input_degree.sort()
	dfsize = len(input_degree)
	freq_degree = freq_dist(degree, dfsize)
	f_outDegree.sort()
	input_f_outDegree = list(set(f_outDegree))
	input_f_outDegree.sort()
	f_ofsize = len(input_f_outDegree)
	freq_f_outDegree = freq_dist(f_outDegree, f_ofsize)
	f_degree.sort()
	input_f_degree = list(set(f_degree))
	input_f_degree.sort()
	f_dfsize = len(input_f_degree)
	freq_f_degree = freq_dist(f_degree, f_dfsize)
	#determine difference between Forest Fire values and originals
	#make master degree list for each degree type
	t = []
	for i in input_f_inDegree:
		t.append(i)
	for i in input_inDegree:
		t.append(i)
	inMaster = list(set(t))
	inMaster.sort()
	s = []
	for j in input_f_outDegree:
		s.append(j)
	for j in input_outDegree:
		s.append(j)
	outMaster = list(set(s))
	outMaster.sort()
	r = []
	for k in input_f_degree:
		r.append(k)
	for k in input_degree:
		r.append(k)
	degMaster = list(set(r))
	degMaster.sort()
	#fix frequency lists to included zeros for values in the master list but not the original for comparison purposes
	j = 0
	i = 0
	new_freq_inDegree = []
	for i in range(len(inMaster)):
		if i >= len(input_inDegree):
			new_freq_inDegree.append(0)
			continue
		if inMaster[i] == input_inDegree[j]:
			new_freq_inDegree.append(freq_inDegree[j])
			j = j + 1
			continue
		else:
			new_freq_inDegree.append(0)
	j = 0
	i = 0
	new_freq_f_inDegree = []
	for i in range(len(inMaster)):
		if i >= len(input_f_inDegree):
			new_freq_f_inDegree.append(0)
			continue
		if inMaster[i] == input_f_inDegree[j]:
			new_freq_f_inDegree.append(freq_f_inDegree[j])
			j = j + 1
		else:
			new_freq_f_inDegree.append(0)
	j = 0
	i = 0
	new_freq_outDegree = []
	for i in range(len(outMaster)):
		if i >= len(input_outDegree):
			new_freq_outDegree.append(0)
			continue
		if outMaster[i] == input_outDegree[j]:
			new_freq_outDegree.append(freq_outDegree[j])
			j = j + 1
		else:
			new_freq_outDegree.append(0)
	j = 0
	i = 0
	new_freq_f_outDegree = []
	for i in range(len(outMaster)):
		if i >= len(input_f_outDegree):
			new_freq_f_outDegree.append(0)
			continue
		if outMaster[i] == input_f_outDegree[j]:
			new_freq_f_outDegree.append(freq_f_outDegree[j])
			j = j + 1
		else:
			new_freq_f_outDegree.append(0)
	j = 0
	i = 0
	new_freq_degree = []
	for i in range(len(degMaster)):
		if i >= len(input_degree):
			new_freq_degree.append(0)
			continue
		if degMaster[i] == input_degree[j]:
			new_freq_degree.append(freq_degree[j])
			j = j + 1
		else:
			new_freq_degree.append(0)
	j = 0
	i = 0
	new_freq_f_degree = []
	for i in range(len(degMaster)):
		if i >= len(input_f_degree):
			new_freq_f_degree.append(0)
			continue
		if degMaster[i] == input_f_degree[j]:
			new_freq_f_degree.append(freq_f_degree[j])
			j = j + 1
		else:
			new_freq_f_degree.append(0)
	#calculate differences between frequencies for each degree value
	diff = []
	indiff = []
	outdiff = []
	k = 0
	for k in range(len(inMaster)):
		indiff.append(abs(new_freq_f_inDegree[k] - new_freq_inDegree[k]))
	k = 0
	for k in range(len(outMaster)):
		outdiff.append(abs(new_freq_f_outDegree[k] - new_freq_outDegree[k]))
	k = 0
	for k in range(len(degMaster)):
		diff.append(abs(new_freq_f_degree[k] - new_freq_degree[k]))
	#Since the distribution of frequencies forms and exponential curve, x values are replaced with log(y)
	#so that the distribution forms a straight line.
	log_inDegree = take_log(input_inDegree)
	log_outDegree = take_log(input_outDegree)
	log_degree = take_log(input_degree)
	log_freq_inDegree = take_log(freq_inDegree)
	log_freq_outDegree = take_log(freq_outDegree)
	log_freq_degree = take_log(freq_degree)
	log_f_inDegree = take_log(input_f_inDegree)
	log_f_outDegree = take_log(input_f_outDegree)
	log_f_degree = take_log(input_f_degree)
	log_freq_f_inDegree = take_log(freq_f_inDegree)
	log_freq_f_outDegree = take_log(freq_f_outDegree)
	log_freq_f_degree = take_log(freq_f_degree)
	#log_inMaster = take_log(inMaster)
	#log_indiff = take_log(indiff)
	#log_outMaster = take_log(outMaster)
	#log_outdiff = take_log(outdiff)
	#log_degMaster = take_log(degMaster)
	#log_diff = take_log(diff)
	#plot results
	fig = plt.figure(figsize=(8,16))
	fig.suptitle(f_in_files[x][29:(len(f_in_files[x])-26)])
	idg = fig.add_subplot(411)
	idg.set_xlabel('Log Degree In')
	idg.set_ylabel('Log Frequency')	
	idg.set_xscale('log')
	idg.set_yscale('log')
	idg.scatter(log_inDegree, log_freq_inDegree, s=20, c='b', marker='o', label='Original')
	idg.scatter(log_f_inDegree, log_freq_f_inDegree, s=20, c='r', marker='o', label='Forest Fire')
	#idg.plot(log_inDegree, log_freq_inDegree,'b', label='Original') 
	#idg.plot(log_k_inDegree, log_freq_k_inDegree, 'r', label='Kronecker')
	idg.legend(loc='lower left')
	plt.xlim(0,10)
	odg = fig.add_subplot(412)
	odg.set_xlabel('Log Degree Out')
	odg.set_ylabel('Log Frequency')
	odg.set_xscale('log')
	odg.set_yscale('log')
	#odg.plot(log_outDegree, log_freq_outDegree, 'b', label='Original')
	#odg.plot(log_k_outDegree, log_freq_k_outDegree, 'r', label='Kronecker')
	odg.scatter(log_outDegree, log_freq_outDegree, s=20, c='b', marker='o', label='Original')
	odg.scatter(log_f_outDegree, log_freq_f_outDegree, s=20, c='r', marker='o', label='Forest Fire')	
	#odg.legend()
	plt.xlim(0,10)
	dg = fig.add_subplot(413)
	dg.set_xlabel('Log Degree')
	dg.set_ylabel('Log Frequency')
	dg.set_xscale('log')
	dg.set_yscale('log')
	#dg.plot(log_degree, log_freq_degree, 'b', label='Original')
	#dg.plot(log_k_degree, log_freq_k_degree, 'r', label='Kronecker')
	dg.scatter(log_degree, log_freq_degree, s=20, c='b', marker='o', label='Original')
	dg.scatter(log_f_degree, log_freq_f_degree, s=20, c='r', marker='o', label='Forest Fire')
	#dg.legend()
	plt.xlim(0,10)
	d = fig.add_subplot(414)
	d.set_xlabel('Degree')
	d.set_ylabel('Frequency Difference')
	#d.set_xscale('log')
	#d.set_yscale('log')
	d.plot(inMaster, indiff, 'b', label='In Degree')
	d.plot(outMaster, outdiff, 'r', label='Out Degree')
	d.plot(degMaster, diff, 'g', label='Degree')
	plt.xlim(0,20)
	d.legend(loc='best')
	fig.tight_layout()
	plt.savefig('ff_log_{}.png'.format(f_in_files[x][29:(len(f_in_files[x])-26)]))
	
