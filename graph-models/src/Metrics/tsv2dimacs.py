#!/usr/bin/env python3
import os
import sys

class IdGenerator:
    def __init__(self):
        self.hashtable = dict()

    def getId(self, item):
        if item in self.hashtable:
            return self.hashtable[item] 
        else:
            id = str(len(self.hashtable) + 1)
            self.hashtable[item] = id
            return id

    def count(self):
        return len(self.hashtable)

def convert2dimacs(path):
    num_edges = 0
    id_generator = IdGenerator()

    f = open(path, 'r')
    for line in f:
        num_edges += 1
        tokens = line.split(' ')
        id_generator.getId(tokens[0])
        id_generator.getId(tokens[1])
    f.close()

    num_vertices = id_generator.count()
    outpath = path + '.dimacs'

    f = open(path, 'r')
    print('Writing file: ' + outpath)
    fout = open(outpath, 'w')
    fout.write('p sp ' + str(num_vertices) + \
            ' ' + str(num_edges) + '\n')

    for line in f:
        num_edges += 1
        tokens = line.split(' ')
        u = id_generator.getId(tokens[0])
        v = id_generator.getId(tokens[1])
        if len(tokens) == 3:
            fout.write('a ' + str(u) + ' ' + str(v) + \
                    ' ' + tokens[2])
        else:
            fout.write('a ' + str(u) + ' ' + str(v) + ' 1\n')
    f.close()
    fout.close() 

inputs = []
if len(sys.argv) > 1:
    if len(sys.argv) == 2:
        inp = sys.argv[1]
        if inp.find('.tsv') != -1:
            inputs.append(inp)
        elif os.path.isdir(inp):
            files = os.listdir(inp)
            for f in files:
                if f.find('.tsv') != -1:
                    inputs.append(inp + '/' + f)
    else:
        for i in range(1, len(sys.argv)):
            inputs.append(sys.argv[i])
else:
    for line in sys.stdin:
        inputs.append(line.strip())

for file in inputs:
    convert2dimacs(file)
