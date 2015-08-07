#!/usr/bin/python
import os,sys

def process_pagerank(dirpath, prefix):
    vertex_rank = []
    rank_list = []
    for i in range(1,5):
        filepath = dirpath + '/' + prefix + str(i) + '_of_4'
        #print('Processing ' + filepath)
        f = open(filepath, 'r')
        for line in f:
            tokens = line.strip().split('\t')
            #vertex_rank[tokens[0]] = tokens[1]
            vertex_rank.append(float(tokens[1]))
            rank_list.append([tokens[1], tokens[0])
        f.close()
    sorted_rank = sorted(vertex_rank, reverse=True) 
    sorted_rank_list = sorted(rank_list, reverse=True)
    str_rank_array = [str(sorted_rank[i][0]) for i in range(100)]
    str_node_array = [str(sorted_rank[i][1]) for i in range(100)]
    out_str = ','.join(str_rank_array)
    print(out_str)
def process_dir(logdir):
    dirpath = logdir + '/pagerank'
    files = os.listdir(logdir)
    for f in files:
        if f.find('.log') != -1:
            prefix = f.replace('.pagerank.log', '_pagerank_')
            process_pagerank(dirpath, prefix) 

process_dir(sys.argv[1])
