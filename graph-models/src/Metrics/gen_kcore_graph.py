#!/usr/bin/env python3
import os, sys
import gmetrics_lib

def csv2tsv(path):
    f = open(path)
    ip_map = dict()
    outpath = path.replace('csv', 'tsv')
    f_out = open(outpath, 'w')
    print(outpath)
    for line in f:
        tokens = line.strip().split(', ')
        src = tokens[0]
        dst = tokens[1]
        if src not in ip_map:
            id = str(len(ip_map))
            ip_map[src] = id
        else:
            id = ip_map[src]
        u = id
        if dst not in ip_map:
            id = str(len(ip_map))
            ip_map[dst] = id
        else:
            id = ip_map[dst]
        v = id
        f_out.write(u + str(' ') + v + '\n')
    f.close()
    f_out.close()

if len(sys.argv) < 3:
    print('USAGE:')
    print(' ' + sys.argv[0] + ' <directory with tsv files (FORMAT: "u v")> <k-core count, e.g. 500>')
    print(' A subdirectory named kcore_graphs will be created in the directory with tsv files')
    sys.exit(1)

tsv_dir = sys.argv[1]
files = os.listdir(tsv_dir)
#kcores = ['10', '50', '100', '500']
kcores = [sys.argv[2]]
kcore_graph_dir = tsv_dir + '/kcore_graphs/'
gmetrics_lib.mkdir_p(kcore_graph_dir)

for f in files:
    if f.find('.tsv') != -1:
        #csv2tsv(f)
        #outpath = f.replace('csv', 'tsv')
        inpath = tsv_dir + '/' + f
        tokens = f.split('.')
        prefix = tokens[0]
        kcore_prefix = kcore_graph_dir + 'kcore_' + prefix
        for k in kcores:
            cmd = 'kcore --graph ' + inpath + \
            ' --kmin ' + k + ' --kmax ' + k + \
            ' --savecores ' + kcore_prefix + ' --format tsv'
            os.system(cmd)
            graph_prefix = kcore_prefix + '.' + k
            kcore_graph = graph_prefix + '.tsv'
            file_list = os.listdir(kcore_graph_dir)
            f_out = open(kcore_graph, 'w')
            for kcore_f in file_list:
                kcore_out_path = kcore_graph_dir + kcore_f
                if kcore_out_path.find(graph_prefix) != -1:
                    f_in = open(kcore_out_path)
                    for line in f_in:
                        tokens = line.split('\t')
                        f_out.write(tokens[0] + ' ' + tokens[1])
                    f_in.close()
                    os.remove(kcore_out_path)
            f_out.close()
