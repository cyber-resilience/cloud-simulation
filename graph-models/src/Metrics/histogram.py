#!/usr/bin/env python3
""" Providing histogram functions"""
import math
import gmetrics_lib

def get_variance(numbers):
    """ Returns the variance from a list of numbers """
    list_size = len(numbers)
    if list_size == 0:
        return 0
    sum = 0.0
    for n in numbers:
        sum += float(n/list_size)
    mean = sum
    sum = 0.0
    for n in numbers:
        sum += float(((n-mean)*(n-mean)/(list_size-1)))
    return sum

# 
# Im
def equi_depth_histogram(num_list, num_bins):
    """ 
    Computes an equi-depth histogram.  Given a list of numbers and the number
    of target bins, it returns the bins of the histogram.
    """
    # set the range
    min_v = min(num_list)
    max_v = max(num_list)
    init_bin_count = 100
    bin_width = (max_v - min_v)/init_bin_count
    init_histogram = [0]*init_bin_count
    init_bins = []

    # create initial bins
    for i in range(init_bin_count):
        beg = min_v + i*bin_width
        end = min_v + (i+1)*bin_width
        init_bins.append([beg, end])

    # populate the bin counts
    for n in num_list:
        if n == max_v:
            bin_id = init_bin_count -1
        else:
            bin_id = int((n - min_v)/bin_width)
        init_histogram[bin_id] += 1 

    # filter out empty bins
    bins = []
    histogram = []
    for i in range(init_bin_count):
        if init_histogram[i] != 0:
            bins.append(init_bins[i])
            histogram.append(init_histogram[i])

    running_count = 0 
    while len(bins) > num_bins:
        h_len = len(histogram)
        curr_variance = get_variance(histogram)
        candidates = []
        # for each merge candidate, compute the reduction in variance
        for i in range(h_len-1):
            cost = histogram[i] + histogram[i+1]
            tmp_list = []
            tmp_list.extend(histogram[0:i])
            tmp_list.append(cost)
            tmp_list.extend(histogram[i+2:])
            new_variance = get_variance(tmp_list)
            variance_reduc = curr_variance - new_variance
            candidates.append([variance_reduc, i]) 

        # choose the merge candidate that provides maximum variance reduction
        candidates = sorted(candidates, reverse=True)
        i = candidates[0][1]
        # merge to create new bins and count array 
        merged_count = histogram[i] + histogram[i+1]
        new_histogram = []
        new_histogram.extend(histogram[0:i])
        new_histogram.append(merged_count)
        new_histogram.extend(histogram[i+2:])
        merged_bin = [ bins[i][0] , bins[i+1][1] ]
        new_bins = []
        new_bins.extend(bins[0:i])
        new_bins.append(merged_bin)
        new_bins.extend(bins[i+2:])
        # iterate again
        histogram = new_histogram
        bins = new_bins
    return bins

def get_feature(bins, v_str):
    """Given the bins of a histogram, this function maps the input to a bin id"""
    v = float(v_str)
    bin_index = -1
    i = 0
    for bin in bins:
        # bin is a 2-element tuple containing the low and high range
        if bin[0] <= v and v < bin[1]:
            bin_index = i
            break
        else:
            i += 1
    if bin_index == -1:
        max = bins[-1][1]
        if v >= max:
            bin_index = len(bins)-1 
        else:
            print('Failed to map: ' + v_str)
    assert bin_index != -1
    return bin_index 

class FeatureMapper:
    def __init__(self, node_feature_dict):
        feature_values = []
        for (k,v) in node_feature_dict.items():
            feature_values.append(float(v))
        self.bins = equi_depth_histogram(feature_values, 3)
        return
            
    def map(self, val):
        return get_feature(self.bins, val)
            
def test_histogram():
    triangle_stats = dict()
    path = '/pic/projects/mnms4graphs/iscx/tsv/testbed-11jun-aggr.tsv'
    #path = 'test.tsv'
    gmetrics_lib.get_triangles(path, triangle_stats)
    array = []
    fout = open('out-deg.dat', 'w')
    for k, v in triangle_stats.items():
        # read out degree
        array.append(int(v[-1]))
        fout.write(str(v[-1]) + '\n')
    fout.close()
    #array = [1, 2, 3, 4, 5, 6]
    #array = [[10,-1], [0, 1], [-1, -1]]
    #print(sorted(array))
    equi_height_histogram(array, 2)
    equi_height_histogram(array, 3)
    equi_height_histogram(array, 4)
    return
