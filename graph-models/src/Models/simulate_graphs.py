#!/usr/bin/python
import networkx as nx
import sys

def convert_edgelist_to_graphviz(inpath):
    outpath = inpath.replace('.txt', '.dot')
    fin = open(inpath)
    fout = open(outpath, 'w')
    fout.write('graph model {\n')
    for line in fin:
        tokens = line.split(' ')
        fout.write(tokens[0] + ' -- ' + tokens[1] + '\n')
    fin.close()
    fout.write('}\n')
    fout.close()

#print('Generating [Balanced Tree]')
#r = 5
#h = 4
#balanced_tree = nx.balanced_tree(r, h)
#outpath = 'balanced_tree_r' + str(r) + '_h' + str(h) + '.txt'
#nx.write_edgelist(balanced_tree, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

#print('Generating [Barbell Graph]')
#n1 = 8
#n2 = 1
#barbell_graph = nx.barbell_graph(n1, n2)
#outpath = 'barbell_graph_' + str(n1) + '_' + str(n2) + '.txt'
#nx.write_edgelist(barbell_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)
#
#print('Generating [Complete Bipartite Graph]')
#n1 = 100
#n2 = 20
#bipartite_graph = nx.complete_bipartite_graph(n1, n2)
#outpath = 'complete_bip_graph_' + str(n1) + '_' + str(n2) + '.txt'
#nx.write_edgelist(bipartite_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

#print('Generating [Grid Graph]')
#n1 = 3
#n2 = 4
#grid_graph = nx.grid_graph([n1, n2])
#outpath = 'grid_graph_' + str(n1) + '_' + str(n2) + '.txt'
#nx.write_edgelist(grid_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

#print('Generating [2-d Grid Graph]')
#n1 = 2
#n2 = 3
#grid_2d_graph = nx.grid_2d_graph(n1, n2)
#outpath = 'grid_graph_' + str(n1) + '_' + str(n2) + '.txt'
#nx.write_edgelist(grid_2d_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

#print('Generating [Hypercube Graph]')
#n1 = 4
#hypercube_graph = nx.hypercube_graph(n1)
#outpath = 'hypercube_graph_' + str(n1) + '.txt'
#nx.write_edgelist(hypercube_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

#print('Generating [Star Graph]')
#n1 = 100
#star_graph = nx.star_graph(n1)
#outpath = 'star_graph_' + str(n1) + '.txt'
#nx.write_edgelist(star_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

#print('Generating [Lollipop Graph]')
#k_m = 4
#p_n = 3
#lollipop_graph = nx.lollipop_graph(k_m, p_n)
#outpath = 'lollipop_graph_' + str(k_m) + '_' + str(p_n) + '.txt'
#nx.write_edgelist(lollipop_graph, outpath, data=False)
#convert_edgelist_to_graphviz(outpath)

print('Generating [Dorogovtsev-Goltsev-Mendes Graph]')
n = 20
dgm_graph = nx.dorogovtsev_goltsev_mendes_graph(n)
outpath = 'dgm_graph_' + str(n) + '.txt'
nx.write_edgelist(dgm_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)
sys.exit(0)
print('Generating [Erdos-Renyi Graph]')
n = 100
p = 0.7
erdos_renyi_graph = nx.erdos_renyi_graph(n, p)
outpath = 'erdos_renyi_graph_' + str(n) + '.txt'
nx.write_edgelist(erdos_renyi_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)

print('Generating [Preferential Attachment Model Graph]')
n = 100
m = 5
prerential_attachment_graph = nx.barabasi_albert_graph(n, m)
outpath = 'preferential_attachment_graph_' + str(n) + '_' + str(m) + '.txt'
nx.write_edgelist(prerential_attachment_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)

print('Generating [Powerlaw Cluster Graph]')
n = 100
m = 5
powerlaw_cluster_graph = nx.powerlaw_cluster_graph(n, m, 0.7)
outpath = 'powerlaw_cluster_graph_' + str(n) + '_' + str(m) + '.txt'
nx.write_edgelist(powerlaw_cluster_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)

print('Generating [Random Lobster]')
n = 100
lobster_graph = nx.random_lobster(n, 0.7, 0.7)
outpath = 'random_lobster_graph_' + str(n) + '.txt'
nx.write_edgelist(lobster_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)

print('Generating [Powerlaw Tree]')
n = 100
powerlaw_tree = nx.random_powerlaw_tree(n, 3, None, 10000)
outpath = 'powerlaw_tree_' + str(n) + '.txt'
nx.write_edgelist(powerlaw_cluster_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)

print('Generating [Bipartite Random Graph]')
n = 100
m = 20
bipartite_random_graph = nx.bipartite_random_graph(n, m, 0.7)
outpath = 'bipartite_random_graph_' + str(n) + '_' + str(m) + '.txt'
nx.write_edgelist(bipartite_random_graph, outpath, data=False)
convert_edgelist_to_graphviz(outpath)
