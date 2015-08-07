#!/usr/bin/python
import sys

def load_node_data(file, node_data):
    f = open(file, 'r')
    for line in f:
        tokens = line.strip().split(' ')
        u = tokens[0]
        v = tokens[1]
        if u in node_data:
            node_data[u] += 1
        else:
            node_data[u] = 1
        if v in node_data:
            node_data[v] += 1
        else:
            node_data[v] = 1
    f.close()

def load_partition_data(file, node_partition):
    f = open(file, 'r')
    print('Loading partition: ' + file)
    for line in f:
        tokens = line.strip().split('\t')
        comp_id = tokens[1]
        node_id = tokens[0]
        if comp_id in node_partition:
            node_partition[comp_id].append(node_id)
        else:
            node_partition[comp_id] = [node_id]
    f.close()

def store_json(outpath, node_partition, node_data):
    f = open(outpath, 'w') 
    print('Number of components = ' + str(len(node_partition)))
    f.write('{\n')
    f.write('\"name\": \"' + outpath + '\",\n')
    f.write('\"children\": [\n')
    for comp_id in node_partition:
        f.write('{\n')
        f.write('\"name\": \"' + str(comp_id) + '\",\n')
        f.write('\"children\": [\n')
        children = node_partition[comp_id]

        node_weight_v = []
        for c in children:
            node_weight_v.append([node_data[c], c])
        cost_v = sorted(node_weight_v, reverse=True) 
        num_children = len(children)
        if num_children > 20:
            disp_children = 20
        else:
            disp_children = num_children
        max_nodes = disp_children-1
        node_count = 0
        for i in range(max_nodes):
            node = cost_v[i][1] # children[i]
            size = str(cost_v[i][0]) # str(node_data[node])
            f.write('{\"name\": \"' + str(node) + '\", \"size\": ' + size + '},\n')
        node = cost_v[max_nodes][1] #children[max_nodes]
        size = str(cost_v[max_nodes][0]) #str(node_data[node])
        f.write('{\"name\": \"' + str(node) + '\", \"size\": ' + size + '}\n')
        f.write(']\n')
        f.write('},\n')
    f.write(']\n')
    f.write('}\n')
    f.close()

def store_multiscale_json(file, out_prefix):
    node_partition = dict()
    node_data = dict()
    load_node_data(file, node_data)
    partition_file = file + '.result_1_of_1'
    load_partition_data(partition_file, node_partition)
    outpath = 'multi_scale_' + out_prefix + '.json'
    store_json(outpath, node_partition, node_data)

if len(sys.argv) < 3:
    print('Usage: ' + sys.argv[0] + ' <graph_file> <out_prefix>')
else:
    store_multiscale_json(sys.argv[1], sys.argv[2])
