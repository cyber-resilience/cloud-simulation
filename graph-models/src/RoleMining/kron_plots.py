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
k_in_file_list = open(sys.argv[4], 'r')
k_in_files = k_in_file_list.readlines()
k_in_file_list.close()
k_out_file_list = open(sys.argv[5], 'r')
k_out_files = k_out_file_list.readlines()
k_out_file_list.close()
k_deg_file_list = open(sys.argv[6], 'r')
k_deg_files = k_deg_file_list.readlines()
k_deg_file_list.close()


#process run for each file
for x in range(len(in_files)):
	#open the file containing the node and degree information
	F = open(str.strip(in_files[x]), 'r')
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
	F = open(str.strip(k_in_files[x]), 'r')
	#initialize lists to store node and degree information
	k_nodes = []
	k_inDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		k_nodes.append(int(tmp[0]))
		k_inDegree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(out_files[x]), 'r')
	#initialize lists to store node and degree information
	outDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		outDegree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(k_out_files[x]), 'r')
	#initialize lists to store node and degree information
	k_outDegree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		k_outDegree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(deg_files[x]), 'r')
	#initialize lists to store node and degree information
	degree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		degree.append(int(tmp[1]))
	F.close()
	F = open(str.strip(k_deg_files[x]), 'r')
	#initialize lists to store node and degree information
	k_degree = []
	#read in each line and store value to appropriate lists
	for line in F:
		tmp = line.split()
		#for i in tmp:
		#	i = int(i)
		k_degree.append(int(tmp[1]))
	F.close()
	#sort each list so that instances of the same value will be adjacent to each other
	inDegree.sort()
	k_inDegree.sort()
	#convert list to a set to remove duplicates
	input_inDegree = list(set(inDegree))
	input_k_inDegree = list(set(k_inDegree))
	#determine number of different values for which frequency will be computed
	ifsize = len(input_inDegree)
	k_ifsize = len(input_k_inDegree)
	#compute the frequency of each value in the list and store the results in a new list
	freq_inDegree = freq_dist(inDegree, ifsize)
	freq_k_inDegree = freq_dist(k_inDegree, k_ifsize)
	#repeat above for remaining lists
	outDegree.sort()
	input_outDegree = list(set(outDegree))
	ofsize = len(input_outDegree)
	freq_outDegree = freq_dist(outDegree, ofsize)
	degree.sort()
	input_degree = list(set(degree))
	dfsize = len(input_degree)
	freq_degree = freq_dist(degree, dfsize)
	k_outDegree.sort()
	input_k_outDegree = list(set(k_outDegree))
	k_ofsize = len(input_k_outDegree)
	freq_k_outDegree = freq_dist(k_outDegree, k_ofsize)
	k_degree.sort()
	input_k_degree = list(set(k_degree))
	k_dfsize = len(input_k_degree)
	freq_k_degree = freq_dist(k_degree, k_dfsize)
	#Since the distribution of frequencies forms and exponential curve, x values are replaced with log(y)
	#so that the distribution forms a straight line.
	log_inDegree = take_log(input_inDegree)
	log_outDegree = take_log(input_outDegree)
	log_degree = take_log(input_degree)
	log_freq_inDegree = take_log(freq_inDegree)
	log_freq_outDegree = take_log(freq_outDegree)
	log_freq_degree = take_log(freq_degree)
	log_k_inDegree = take_log(input_k_inDegree)
	log_k_outDegree = take_log(input_k_outDegree)
	log_k_degree = take_log(input_k_degree)
	log_freq_k_inDegree = take_log(freq_k_inDegree)
	log_freq_k_outDegree = take_log(freq_k_outDegree)
	log_freq_k_degree = take_log(freq_k_degree)
	#best fit line is computed for the data and the slope saved to a file
	#c = np.polyfit(log_inDegree, log_freq_inDegree, 1)
	#c = np.polyfit(log_outDegree, log_freq_outDegree, 1)
	#c = np.polyfit(log_degree, log_freq_degree, 1)
	#plots are generated to display the frequency distributions for degree in, degree out and overall degree
	#fig = plt.figure()
	#fig.suptitle(in_files[x][30:])
	#idg = fig.add_subplot(311)
	#idg.set_xlabel('Log Degree In')
	#idg.set_ylabel('Log Frequency')	
	#idg.set_xscale('log')
	#idg.set_yscale('log')
	#idg.plot(log_inDegree, log_freq_inDegree,'b', label='Original') 
	#idg.plot(log_k_inDegree, log_freq_k_inDegree, 'r', label='Kronecker')
	#idg.legend(loc='upper right')
	#plt.xlim(min(log_inDegree),10)
	#odg = fig.add_subplot(312)
	#odg.set_xlabel('Log Degree Out')
	#odg.set_ylabel('Log Frequency')
	#odg.set_xscale('log')
	#odg.set_yscale('log')
	#odg.plot(log_outDegree, log_freq_outDegree, 'b', label='Original')
	#odg.plot(log_k_outDegree, log_freq_k_outDegree, 'r', label='Kronecker')
	#odg.legend()
	#plt.xlim(min(log_outDegree),10)
	#dg = fig.add_subplot(313)
	#dg.set_xlabel('Log Degree')
	#dg.set_ylabel('Log Frequency')
	#dg.set_xscale('log')
	#dg.set_yscale('log')
	#dg.plot(log_degree, log_freq_degree, 'b', label='Original')
	#dg.plot(log_k_degree, log_freq_k_degree, 'r', label='Kronecker')
	#dg.legend()
	#plt.xlim(min(log_degree),10)
	#fig.tight_layout()
	#plt.savefig('kron_log_{}.png'.format(in_files[x][30:]))
	fig = plt.figure()
	fig.suptitle(in_files[x][30:])
	idg = fig.add_subplot(311)
	idg.set_xlabel('Log Degree In')
	idg.set_ylabel('Log Frequency')	
	idg.set_xscale('log')
	idg.set_yscale('log')
	idg.scatter(log_inDegree, log_freq_inDegree, s=20, c='b', marker='o', label='Original')
	idg.scatter(log_k_inDegree, log_freq_k_inDegree, s=20, c='r', marker='o', label='Kronecker')
	#idg.plot(log_inDegree, log_freq_inDegree,'b', label='Original') 
	#idg.plot(log_k_inDegree, log_freq_k_inDegree, 'r', label='Kronecker')
	idg.legend(loc='lower left')
	plt.xlim(min(log_inDegree),10)
	odg = fig.add_subplot(312)
	odg.set_xlabel('Log Degree Out')
	odg.set_ylabel('Log Frequency')
	odg.set_xscale('log')
	odg.set_yscale('log')
	#odg.plot(log_outDegree, log_freq_outDegree, 'b', label='Original')
	#odg.plot(log_k_outDegree, log_freq_k_outDegree, 'r', label='Kronecker')
	odg.scatter(log_outDegree, log_freq_outDegree, s=20, c='b', marker='o', label='Original')
	odg.scatter(log_k_outDegree, log_freq_k_outDegree, s=20, c='r', marker='o', label='Kronecker')	
	#odg.legend()
	plt.xlim(min(log_outDegree),10)
	dg = fig.add_subplot(313)
	dg.set_xlabel('Log Degree')
	dg.set_ylabel('Log Frequency')
	dg.set_xscale('log')
	dg.set_yscale('log')
	#dg.plot(log_degree, log_freq_degree, 'b', label='Original')
	#dg.plot(log_k_degree, log_freq_k_degree, 'r', label='Kronecker')
	dg.scatter(log_degree, log_freq_degree, s=20, c='b', marker='o', label='Original')
	dg.scatter(log_k_degree, log_freq_k_degree, s=20, c='r', marker='o', label='Kronecker')
	#dg.legend()
	plt.xlim(min(log_degree),10)
	fig.tight_layout()
	plt.savefig('kron_log_{}.png'.format(in_files[x][28:(len(in_files[x])-15)]))
	
