#!/usr/bin/env python3
import os
import sys
import flow_lib

def transform_tsv(path):
    print('Processing ' + path)
    fout = open(path + '.norm.tsv', 'w')
    fin = open(path)
    mapper = flow_lib.HashedIdMapper()
    for line in fin:
        tokens = line.strip().split(' ')
        fout.write(mapper.map(tokens[0]) + ',' + mapper.map(tokens[1]) + '\n')
    fin.close()
    fout.close()

tsvdir = sys.argv[1]
files = os.listdir(tsvdir)
for f in files:
    if f.find('.tsv') != -1:
        transform_tsv(tsvdir + '/' + f)
