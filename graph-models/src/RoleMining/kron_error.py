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

output = open('Kron-plogon-error.txt', 'w')
#process run for each file
for x in range(len(in_files)):
	output.write(str.strip(k_in_files[x])+'\n')
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
	input_inDegree.sort()
	input_k_inDegree = list(set(k_inDegree))
	input_k_inDegree.sort()
	#determine number of different values for which frequency will be computed
	ifsize = len(input_inDegree)
	k_ifsize = len(input_k_inDegree)
	#compute the frequency of each value in the list and store the results in a new list
	freq_inDegree = freq_dist(inDegree, ifsize)
	freq_k_inDegree = freq_dist(k_inDegree, k_ifsize)
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
	k_outDegree.sort()
	input_k_outDegree = list(set(k_outDegree))
	input_k_outDegree.sort()
	k_ofsize = len(input_k_outDegree)
	freq_k_outDegree = freq_dist(k_outDegree, k_ofsize)
	k_degree.sort()
	input_k_degree = list(set(k_degree))
	input_k_degree.sort()
	k_dfsize = len(input_k_degree)
	freq_k_degree = freq_dist(k_degree, k_dfsize)
	#determine difference between Kronecker values and originals
	#make master degree list for each degree type
	t = []
	for i in input_k_inDegree:
		t.append(i)
	for i in input_inDegree:
		t.append(i)
	inMaster = list(set(t))
	inMaster.sort()
	s = []
	for j in input_k_outDegree:
		s.append(j)
	for j in input_outDegree:
		s.append(j)
	outMaster = list(set(s))
	outMaster.sort()
	r = []
	for k in input_k_degree:
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
	new_freq_k_inDegree = []
	for i in range(len(inMaster)):
		if i >= len(input_k_inDegree):
			new_freq_k_inDegree.append(0)
			continue
		if inMaster[i] == input_k_inDegree[j]:
			new_freq_k_inDegree.append(freq_k_inDegree[j])
			j = j + 1
			continue
		else:
			new_freq_k_inDegree.append(0)
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
			continue
		else:
			new_freq_outDegree.append(0)
	j = 0
	i = 0
	new_freq_k_outDegree = []
	for i in range(len(outMaster)):
		if i >= len(input_k_outDegree):
			new_freq_k_outDegree.append(0)
			continue
		if outMaster[i] == input_k_outDegree[j]:
			new_freq_k_outDegree.append(freq_k_outDegree[j])
			j = j + 1
			continue
		else:
			new_freq_k_outDegree.append(0)
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
			continue
		else:
			new_freq_degree.append(0)
	j = 0
	i = 0
	new_freq_k_degree = []
	for i in range(len(degMaster)):
		if i >= len(input_k_degree):
			new_freq_k_degree.append(0)
			continue
		if degMaster[i] == input_k_degree[j]:
			new_freq_k_degree.append(freq_k_degree[j])
			j = j + 1
			continue
		else:
			new_freq_k_degree.append(0)
	#calculate differences between frequencies for each degree value
	in_rel_error = []
	in_abs_error = []
	out_rel_error = []
	out_abs_error = []
	rel_error = []
	abs_error = []
	k = 0
	for k in range(len(inMaster)):
		error = (abs(new_freq_k_inDegree[k] - new_freq_inDegree[k]))
		in_abs_error.append(error)
		if error == 0:
			in_rel_error.append(0.0)
			continue
		if new_freq_inDegree[k] == 0:
			#print 'Absolute Error: {}'.format(error)
			continue
		in_rel_error.append(float(error)/float(new_freq_inDegree[k]))
	k = 0
	for k in range(len(outMaster)):
		error = (abs(new_freq_k_outDegree[k] - new_freq_outDegree[k]))
		out_abs_error.append(error)
		if error == 0:
			out_rel_error.append(0.0)
			continue
		if new_freq_outDegree[k] == 0:
			#print 'Absolute Error: {}'.format(error)
			continue
		out_rel_error.append(float(error)/float(new_freq_outDegree[k]))
	k = 0
	for k in range(len(degMaster)):
		error = (abs(new_freq_k_degree[k] - new_freq_degree[k]))
		abs_error.append(error)
		if error == 0:
			rel_error.append(0.0)
			continue
		if new_freq_degree[k] == 0:
			#print 'Absolute Error: {}'.format(error)
			continue
		rel_error.append(float(error)/float(new_freq_degree[k]))
	ave_in_rel_error = float(sum(in_rel_error))/float(len(in_rel_error))
	#test_in = float(float(sum(in_abs_error))/float(sum(new_freq_inDegree)))/float(len(in_abs_error))
	ave_out_rel_error = float(sum(out_rel_error))/float(len(in_rel_error))
	#test_out = float(float(sum(out_abs_error))/float(sum(new_freq_outDegree)))/float(len(out_abs_error))
	ave_rel_error = float(sum(rel_error))/float(len(rel_error))
	#test = float(float(sum(abs_error))/float(sum(new_freq_degree)))/float(len(abs_error))
	ave_in_abs_error = float(sum(in_abs_error))/float(len(in_abs_error))
	ave_out_abs_error = float(sum(out_abs_error))/float(len(out_abs_error))
	ave_abs_error = float(sum(abs_error))/float(len(abs_error))
	output.write('In Degree Absolute Error: {}\n'.format(ave_in_abs_error))
	output.write('In Degree Relative Error: {}\n'.format(ave_in_rel_error))
	#output.write('In Degree Test Relative Error: {}\n'.format(test_in))
	output.write('Out Degree Absolute Error: {}\n'.format(ave_out_abs_error))
	output.write('Out Degree Relative Error: {}\n'.format(ave_out_rel_error))
	#output.write('Out Degree Test Relative Error: {}\n'.format(test_out))
	output.write('Overall Degree Absolute Error: {}\n'.format(ave_abs_error))
	output.write('Overall Degree Relative Error: {}\n'.format(ave_rel_error))
	#output.write('Overall Degree Test Relative Error: {}\n'.format(test))

output.close()

