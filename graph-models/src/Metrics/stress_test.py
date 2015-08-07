import os, sys
import gmetrics_lib

#data_src = 'unb'
#test_graph = '/pic/projects/mnms4graphs/iscx/netflow/testbed-11jun-aggr.tsv'
#gmetrics_lib.get_graph_size(test_graph)
#data_src = 'evt_logs'
#test_graph = '/pic/projects/mnms4graphs/eventlogs/tsv/plogon20120429.dmp.gr.tsv'
#gmetrics_lib.get_graph_size(test_graph)
#data_src = 'nccdc'
#test_graph = '/pic/projects/mnms4graphs/nccdc/2013/tsv/win3600/nccdc2013_win3600_12.tsv'
#gmetrics_lib.get_graph_size(test_graph)

#sys.exit(1)
test_graph = sys.argv[1]
data_src = os.path.basename(test_graph)
data_src = data_src.replace('.tsv', '')

test_graph_dir = os.path.dirname(test_graph)
tmp_graphs_dir = test_graph_dir + '/tmp-graphs/'
gmetrics_lib.mkdir_p(tmp_graphs_dir)
tmp_graph_prefix = tmp_graphs_dir + 'tmp_graph'

k = get_k(test_graph)
print('Computing top-' + str(k) + ' central nodes')
top_central_nodes = gmetrics_lib.get_top_k_by_centrality(test_graph, k)

op_score = []
[init_nodes, init_edges, init_max_comp_sz] = \
    gmetrics_lib.get_largest_component_size(test_graph)
init_ratio = init_max_comp_sz/init_nodes
op_score.append([0, init_ratio, 1])

curr_graph = test_graph
for i in range(len(top_central_nodes)):
    print('Computing op-ratio for graph ' + str(i+1) + ' of ' + str(k))
    v = top_central_nodes[i]
    next_graph = tmp_graph_prefix + '-' + str(i+1) + '.tsv'
    removed_edges = gmetrics_lib.remove_node_from_graph(curr_graph, next_graph, v) 
    #print('# removed = ' + str(removed_edges))
    if removed_edges == 0:
        continue
    #print(next_graph)
    [num_vertices, num_edges, max_comp_sz] = \
        gmetrics_lib.get_largest_component_size(next_graph)
    #print('# V   = ' + str(num_vertices))
    #print('# E   = ' + str(num_edges))
    #print('# M_c = ' + str(max_comp_sz))
    op_ratio = max_comp_sz/init_nodes
    norm_op_ratio = max_comp_sz/init_max_comp_sz
    edge_loss_fraction = 100*(1-num_edges/init_edges)
    op_score.append([edge_loss_fraction, op_ratio, norm_op_ratio])

    if num_edges == 0:
        break 
    curr_graph = next_graph

gmetrics_lib.rmdir_f(tmp_graphs_dir)

f_log = open('data/op_score_' + data_src + '.csv', 'w')
for t in op_score:
    f_log.write(str(t[0]) + ',' + str(t[1]) + ',' + str(t[2]) + '\n')
f_log.close()
