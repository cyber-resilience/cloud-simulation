import os, shutil, sys
import statistics
from collections import Counter

def logroot():
    #return os.getenv("HOME")
    return '/scratch/sutanay'

#class Counter:
    #def __init__(self):
        #self.hashtable = dict()
#
    #def add(self, item):
        #if item in self.hashtable:
            #self.hashtable[item] += 1
        #else:
            #self.hashtable[item] = 1 
#
    ##def elements(self):
        #return self.hashtable.items()
#
    #def count(self, key):
        #if key in self.hashtable:
            #return self.hashtable[key]
        #else:
            #return -1
#
    #def len(self):
        #return len(self.hashtable.items())
#
def mkdir_p(path):
    try:
        os.makedirs(path)
        #print('INFO Creating directory: ' + path)
    except os.error: 
        pass

def rmdir_f(dirpath):
    shutil.rmtree(dirpath)

def log(str, debug=False):
    if debug:
        print(str)

def get_graph_size(tsv_graph):
    vertex_set = set()
    f = open(tsv_graph)
    num_edges = 0
    for line in f:
        ids = line.strip().split()
        vertex_set.add(ids[0])
        vertex_set.add(ids[1])
        num_edges += 1
    f.close()
    stats = [len(vertex_set), num_edges]
    print('Graph: ' + tsv_graph)
    print('#V = ' + str(stats[0]) + ' #E = ' + str(stats[1]))
    return stats

def get_in_degree_distribution(tsv_graph):
    f = open(tsv_graph)
    in_degree_table = Counter()
    for line in f:
        ids = line.strip().split()
        in_degree_table[ids[1]] += 1
    f.close()
    in_degree_distribution = Counter()
    for v,in_deg in in_degree_table.items():
        in_degree_distribution[in_deg] += 1
    return sorted(in_degree_distribution.items())

def get_avg_in_degree(tsv_graph):
    f = open(tsv_graph)
    in_degree_table = Counter()
    for line in f:
        ids = line.strip().split()
        in_degree_table[ids[1]] += 1
    f.close()
    in_degree_list = []
    for v,in_deg in in_degree_table.items():
        in_degree_list.append(in_deg)
    in_degree_dist = get_in_degree_distribution(tsv_graph)
    for pair in in_degree_dist:
        print(str(pair[0]) + ',' + str(pair[1]))
    print('in degree list size = ' + str(len(in_degree_dist)))
    return statistics.mean(in_degree_list)

def remove_node_from_graph(curr_graph, new_graph, v): 
    removed_edges = 0 
    f_in = open(curr_graph)
    f_out = open(new_graph, 'w')
    v_s = str(v)
    for line in f_in:
        tokens = line.strip().split()
        if tokens[0] != v_s and tokens[1] != v_s:
            f_out.write(line)
        else:
            removed_edges += 1
    f_in.close()
    f_out.close()
    return removed_edges

def get_triangles(path, triangle_stats):
    args = ' --format=tsv --graph=' + path
    logdir = logroot() + '/graphlab/triangles/'
    prefix = logdir + os.path.basename(path) + '_triangles'
    logpath = logdir + 'triangle.log'
    args = ' --per_vertex=' + prefix + args  + ' >& ' + logpath
    cmd = 'directed_triangle_count' + args
    log('Running: ' + cmd)
    mkdir_p(logdir)
    os.system(cmd)

    files = os.listdir(logdir)
    for file in files:
        if file.find('_triangles_') == -1:
            continue
        fin = open(logdir + '/' + file)
        for line in fin:
            tokens = line.strip().split('\t')
            triangle_stats[tokens[0]] = tokens[1:]
        fin.close()
    # cleanup
    #shutil.rmtree(logdir)
    return

def get_centrality(path, centrality_map):
    args = ' --format=tsv --graph=' + path
    logdir = logroot() + '/graphlab/pagerank/'
    prefix = logdir + os.path.basename(path) + '_pagerank'
    logpath = logdir + 'pagerank.log'
    args = ' --saveprefix=' + prefix + args  + ' >& ' + logpath
    cmd = 'pagerank' + args
    log('Running: ' + cmd)
    mkdir_p(logdir)
    os.system(cmd)

    for i in range(1, 5):
        pagerank_file_path = prefix + '_' + str(i) + '_of_4'
        f = open(pagerank_file_path)
        for line in f:
            tokens = line.strip().split('\t')
            centrality_map[tokens[-2]] = float(tokens[-1])
        f.close()

    # cleanup
    shutil.rmtree(logdir)
    return

def get_top_k_by_centrality(path, k, debug=False):

    logdir = logroot() + '/graphlab/pagerank/'
    args = ' --format=tsv --graph=' + path
    prefix = logdir + os.path.basename(path) + '_pagerank'
    logpath = logdir + 'pagerank.log'
    args = ' --saveprefix=' + prefix + args  + ' >& ' + logpath
    cmd = 'pagerank' + args
    log('Running: ' + cmd, debug)
    mkdir_p(logdir)
    os.system(cmd)

    pagerank_vector = []

    for i in range(1, 5):
        pagerank_file_path = prefix + '_' + str(i) + '_of_4'
        f = open(pagerank_file_path)
        for line in f:
            tokens = line.strip().split('\t')
            pagerank_vector.append([float(tokens[-1]), tokens[-2]]) 
        f.close()

    sorted_v = sorted(pagerank_vector, reverse=True)
    top_k_vertices = []
    for i in range(k):
        entry = sorted_v[i]
        top_k_vertices.append(entry[1])

    # cleanup
    shutil.rmtree(logdir)
    return top_k_vertices 

def get_top_k_norm_centrality(path, k, debug=False):

    logdir = logroot() + '/graphlab/pagerank/'
    args = ' --format=tsv --graph=' + path
    prefix = logdir + os.path.basename(path) + '_pagerank'
    logpath = logdir + 'pagerank.log'
    args = ' --saveprefix=' + prefix + args  + ' >& ' + logpath
    cmd = 'pagerank' + args
    log('Running: ' + cmd, debug)
    mkdir_p(logdir)
    os.system(cmd)

    pagerank_vector = []

    for i in range(1, 5):
        pagerank_file_path = prefix + '_' + str(i) + '_of_4'
        f = open(pagerank_file_path)
        for line in f:
            tokens = line.strip().split('\t')
            pagerank_vector.append([float(tokens[-1]), tokens[-2]]) 
        f.close()

    sorted_v = sorted(pagerank_vector, reverse=True)
    top_k_data = []
    for i in range(k):
        entry = sorted_v[i]
        top_k_data.append(sorted_v[i])

    # cleanup
    shutil.rmtree(logdir)
    return top_k_data 

def get_largest_component_size(path, debug=False):

    logdir = logroot() + '/graphlab/connected_comp'
    logfile = logdir + os.path.basename(path) + '.connected_comp.log'
    args = ' --format=tsv --graph=' + path + ' >& '
    cmd = 'connected_component' + args + logfile
    mkdir_p(logdir)
    os.system(cmd)

    log('Parsing: ' + logfile, debug)
    f = open(logfile)
    parse_comps = False
    component_sizes = []
    num_vertices = 0
    num_edges = 0

    for line in f:
        if parse_comps == False:
            if line.find('nverts:') != -1:
                tokens = line.strip().split()
                num_vertices = int(tokens[-1])
            if line.find('nedges:') != -1:
                tokens = line.strip().split()
                num_edges = int(tokens[-1])
            if line.find('size\tcount') != -1: 
                parse_comps = True
        else:
            tokens = line.strip().split()
            component_sizes.append(int(tokens[1]))
    f.close()
    # cleanup
    os.remove(logfile)
    component_sizes = sorted(component_sizes, reverse=True)
    if len(component_sizes) == 0:
        max_comp_size = 0
    else:
        max_comp_size = int(component_sizes[0])

    log([num_vertices, num_edges, max_comp_size], debug)
    return [num_vertices, num_edges, max_comp_size]

def get_kcore_ranking(path):
    kcore_ranking = dict()
    f_graph = open(path)
    for line in f_graph:
        tokens = line.strip().split(' ')
        kcore_ranking[tokens[0]] = 0
        kcore_ranking[tokens[1]] = 0
    f_graph.close()
    print('number of vertices = ' + str(len(kcore_ranking)))

    tsv_dir = os.path.dirname(path)
    filename = os.path.basename(path)
    tokens = filename.split('.')
    prefix = tokens[0]

    logdir = logroot() + '/graphlab/kcore/'
    #kcore_graph_dir = tsv_dir + '/kcore_graphs/'
    kcore_graph_dir = logdir
    mkdir_p(kcore_graph_dir)
    kcore_prefix = kcore_graph_dir + 'kcore_' + prefix

    kcores = [10, 100]
    assign_rank = [1, 2]

    for i in range(len(kcores)):
        k = str(kcores[i])
        rank = assign_rank[i]
        logpath = logdir + 'kcore.log'
        cmd = 'kcore --graph ' + path + \
            ' --kmin ' + k + ' --kmax ' + k + \
            ' --savecores ' + kcore_prefix + ' --format tsv' + \
            ' >& ' + logpath
        os.system(cmd)
        graph_prefix = kcore_prefix + '.' + k 
        file_list = os.listdir(kcore_graph_dir)
        for kcore_f in file_list:
            kcore_out_path = kcore_graph_dir + kcore_f
            if kcore_out_path.find(graph_prefix) != -1: 
                f_in = open(kcore_out_path)
                num_skip = 0
                for line in f_in:
                    tokens = line.strip().split('\t')
                    num_tokens = len(tokens)
                    if num_tokens == 2:
                        #if tokens[0] == ' ' or tokens[1] == ' ':
                            #print('CHECK: ' + line)
                        kcore_ranking[tokens[0]] = rank
                        kcore_ranking[tokens[1]] = rank
                    else:
                        num_skip += 1
                f_in.close()
                #if num_skip > 0:
                    #print('# skipped lines from kcore output: ' + str(num_skip))
                os.remove(kcore_out_path)
        os.remove(logpath)

    shutil.rmtree(kcore_graph_dir)
    return kcore_ranking

def get_approx_diameter(path):
    print('Computing approx diam ...')
    logdir = logroot() + '/graphlab/approx_diameter'
    logfile = logdir + os.path.basename(path) + '.approx_diam.log'
    args = ' --format=tsv --use-sketch=0 --graph=' + path + ' >& '
    cmd = 'approximate_diameter' + args + logfile
    mkdir_p(logdir)
    os.system(cmd)

    approx_diam = 0
    f = open(path, 'r')
    for line in f:
        line = line.strip()
        tokens = line.split()
        if line.find('The approximate diameter is') != -1: 
            approx_diam = int(tokens[-1])
    f.close()
    shutil.rmtree(logdir)
    return approx_diam 
