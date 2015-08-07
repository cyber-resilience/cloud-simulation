#!/usr/bin/env python3
import flow_lib, random, sys
from collections import Counter

# v0.1 - Mon Jul  7 15:13:42 PDT 2014
# providing initial data to Sherman
#
# v0.2 - Mon Jul  7 15:37:35 PDT 2014
# Supports level 0-2

class Attr:
    def __init__(self):
        self.attr_list = []
        return
    def __init__(self, attr_name, attr_val):
        self.attr_list = []
        self.add(attr_name, attr_val)
        return
    def add(self, attr_name, attr_val):
        self.attr_list.append(attr_name + '=' + attr_val)
        return
    def __str__(self):
        return ','.join(self.attr_list)
            
def load_role_map(feature_table_path, role_assignment_path):
    ip_list = []
    role_list = []

    f_features = open(feature_table_path)
    for line in f_features:
        tokens = line.split(' ')
        ip_list.append(tokens[0])    
    f_features.close()
    f_role = open(role_assignment_path)    
    for line in f_role:
        role_list.append(int(line.strip()))
    f_role.close()

    role_map = dict()
    for i in range(len(ip_list)):
        role_map[ip_list[i]] = role_list[i]
    return role_map

def export_attr_graph(outpath, node_attrs, weighted_graph, max_edges, level):
    report_nodes = set()

    for k,v in weighted_graph.most_common(max_edges):
        nodes = k.split(',')
        report_nodes.add(nodes[0])
        report_nodes.add(nodes[1])
    fout = open(outpath, 'w')
    #colors = ['red', 'green', 'blue', 'yellow', 'white']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    if level == 2:
        role_map = load_role_map('data/ds2-unb/features.dat', 'data/ds2-unb/role_assignment.csv')
    
    role_distr = Counter()
    for k in report_nodes:
        node_attr = Attr('count', str(node_attrs[k]))
        if k.find('192.168') != -1 or k.find('10.10.') != -1:
            in_ent = 1
        else:
            in_ent = 0
        node_attr.add('inside', str(in_ent))
        if level == 2:
            #role = int(random.uniform(0,4))
            role = role_map[k]
            role_distr[colors[role]] += 1
            node_attr.add('role', colors[role])
        fout.write('v ' + k + ' [' + str(node_attr) + ']\n')

    for k,v in weighted_graph.most_common(max_edges):
        edge_attr = Attr('weight', str(v))
        fout.write('e ' + k + ' [' + str(edge_attr) + ']\n')
    fout.close()

    #if level == 2:
        #f_out = open('/people/d3m432/dropbox/arc_viz/data.2/roles.csv', 'w')
        #for k,v in role_distr.items():
            #f_out.write(k + ',' + str(v) + '\n')
        #f_out.close()

        #f_out = open('/people/d3m432/dropbox/arc_viz/data.2/spectra1.csv', 'w')
        #for i in range(100):
            #f_out.write(str(random.random()) + '\n')
        #f_out.close()
#
        #f_out = open('/people/d3m432/dropbox/arc_viz/data.2/spectra2.csv', 'w')
        #for i in range(100):
            #f_out.write(str(random.random()) + '\n')
        #f_out.close()

def extract_network_topology(path, outpath, level, max_edges):
    if level == 0:
        num_quads_to_group = 2
    elif level == 1:
        num_quads_to_group = 3
    else:
        num_quads_to_group = 4
    f = open(path)
    weighted_graph = Counter()
    node_attrs = Counter()
    line_count = 0
    for line in f:
        line_count += 1
        if line_count == 1:
            continue
        flow = flow_lib.parse_silk_flow(line)
        if flow == None:
            continue
        src_subnet = flow.get_subnet(True, num_quads_to_group) 
        dst_subnet = flow.get_subnet(False, num_quads_to_group) 
        key = src_subnet + ',' + dst_subnet
        weighted_graph[key] += 1
        node_attrs[src_subnet] += 1
        node_attrs[dst_subnet] += 1
    f.close()
    export_attr_graph(outpath, node_attrs, weighted_graph, max_edges, level)

if len(sys.argv) == 1:
    print('USAGE: ' + sys.argv[0] + ' level [0-2] max-edges (default=100)')
    sys.exit(1)
#path = '/pic/projects/mnms4graphs/iscx/netflow/testbed-11jun-aggr.txt'
path = 'graphs/testbed-11jun-aggr.txt'
#outpath = 'testbed-11jun-aggr.txt.1.graph'
level = int(sys.argv[1])
max_edges = 100
if len(sys.argv) > 2:
    max_edges = int(sys.argv[2])
#outpath = '/people/d3m432/dropbox/arc_viz/data.2/level.' + str(level) + '.graph'
outpath = path + '.level.' + str(level) + '.graph'
extract_network_topology(path, outpath, level, max_edges)
