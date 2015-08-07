#!/usr/bin/env python3
import math
import os
import time
import sys
import statistics
import histogram
import gmetrics_lib
import flow_lib

def process_tsv(prefix_without_tsv):
    tsv_path = prefix_without_tsv + '.tsv'
    id_map_path = tsv_path + '.map' 
    id_mapper = HashedIdMapper()
    id_mapper.load(id_map_path)
    return id_mapper

def transform_unb(path):
    outpath = path + '.tsv'
    mapper = flow_lib.FlowGraphMapper()
    flow_lib.process_flow_data(path, flow_lib.parse_flo, mapper.transform_flow)
    mapper.store_graph(outpath)
    mapper.store_mapping(outpath + '.map')
    return mapper.get_id_mapper()

def transform_eventlog(path):
    outpath = path + '.tsv'
    mapper = flow_lib.FlowGraphMapper()
    flow_lib.process_flow_data(path, flow_lib.parse_event_log, mapper.transform_flow)
    mapper.store_graph(outpath)
    mapper.store_mapping(outpath + '.map')
    return

def map_dict(dict_with_numeric_keys, ip_mapper):
    dict_with_ip_keys = dict()
    for k,v in dict_with_numeric_keys.items():
        ip = ip_mapper.rev_map(k)
        if ip == '':
            continue
        dict_with_ip_keys[ip] = v
        #dict_with_ip_keys[flow_lib.long2ip(int(k))] = v
    return dict_with_ip_keys

def add_feature(node_feature_dict, feature_table, map_feature, init=False):
    if map_feature:
        feature_mapper = histogram.FeatureMapper(node_feature_dict)
    for (k,v) in node_feature_dict.items():
        if init:
            if k not in feature_table:
                feature_table[k] = []
        row = feature_table[k]
        if map_feature:
            row.append(feature_mapper.map(v)) 
        else:
            row.append(v)

def add_feature_list(node_features_dict, feature_table, map_feature, init=False):
    if map_feature == False:
        for (k,v) in node_features_dict.items():
            if init:
                if k not in feature_table:
                    feature_table[k] = []
            row = feature_table[k]
            row.extend(v)
        return

    num_features = 0
    print('Processing feature dictionary with ' + str(len(node_features_dict)) + ' entries')
    for (k,v) in node_features_dict.items():
        num_features = len(v)
        if init:
            if k not in feature_table:
                feature_table[k] = []

    for i in range(num_features):
        print('     processing sub-feature (' + str(i) + ')')
        single_feature_dict = dict()
        for (k,v) in node_features_dict.items():
            single_feature_dict[k] = v[i]
        feature_mapper = histogram.FeatureMapper(single_feature_dict)
        for (k,v) in single_feature_dict.items():
            row = feature_table[k]
            row.append(feature_mapper.map(v)) 
    return

def build_feature_table(flow_path, ip_mapper, feature_table, get_flow_features=True):
    path = flow_path + '.tsv'
    print('Computing triangle based features ...')
    triangle_stats = dict()
    gmetrics_lib.get_triangles(path, triangle_stats)
    ip_triangle_stats = map_dict(triangle_stats, ip_mapper)
    add_feature_list(ip_triangle_stats, feature_table, True, True)
    # in_t out_t through_t cycles out_deg in_deg prank krank inf_s out_s inf_d outf_d
    # role1: Modest out triangles
    # role2: High out degree, modest in degree
    # role3: High in triangles
    # role4: High out degree, modest out triangles
    # role5: High in triangles, low out triangle
    # role6: High in degree 
    # role7: High out flow size

    print('Computing pagerank ...')
    pagerank = dict()
    gmetrics_lib.get_centrality(path, pagerank)
    ip_pagerank = map_dict(pagerank, ip_mapper)
    add_feature(ip_pagerank, feature_table, True)
    print('# ips = ' + str(len(pagerank))) 

    print('Computing kcore ranking ...')
    kcore_ranking = dict()
    kcore_ranking = gmetrics_lib.get_kcore_ranking(path)
    ip_kcore_ranking = map_dict(kcore_ranking, ip_mapper)
    add_feature(ip_kcore_ranking, feature_table, False, True)
    print('# ips [1] = ' + str(len(kcore_ranking))) 
    print('# ips [2] = ' + str(len(ip_kcore_ranking))) 

    if get_flow_features == False:
      return

    print('Computing flow size features ...')
    median_in_flow = dict()
    median_out_flow = dict()
    flow_lib.get_median_flow(flow_path, median_in_flow, median_out_flow, True)
    add_feature(median_in_flow, feature_table, False)
    add_feature(median_out_flow, feature_table, False)
    print('# ips = ' + str(len(median_in_flow))) 
    print('# ips = ' + str(len(median_out_flow))) 

    print('Computing flow duration features ...')
    median_in_flow_duration = dict()
    median_out_flow_duration = dict()
    flow_lib.get_median_flow(flow_path, \
            median_in_flow_duration, median_out_flow_duration, False)
    add_feature(median_in_flow_duration, feature_table, False)
    add_feature(median_out_flow_duration, feature_table, False)
    print('# ips = ' + str(len(median_in_flow_duration))) 
    print('# ips = ' + str(len(median_out_flow_duration))) 

    #mode_protocol = dict()
    #flow_lib.get_mode_protocol(path, mode_protocol)
    #add_feature(mode_protocol, feature_table)

def combine_features(in_degrees, out_degrees, centrality, feature_table):
    for (k,v) in in_degrees.items():
        row = ['-1', '-1', '-1']
        row[0] = str(int(math.log(v, 2)))
        feature_table[k] = row

    for (k,v) in out_degrees.items():
        if k in feature_table:
            row = feature_table[k]
        else:
            row = ['-1', '-1', '-1']
        row[1] = str(int(math.log(v, 2)))

    for (k,v) in centrality.items():
        if k in feature_table:
            row = feature_table[k]
        else:
            row = ['-1', '-1', '-1']
        row[2] = str(int(v/0.1))

def write_feature_matrix(feature_table, out_prefix):
    print('Number of rows in feature matrix : ' + str(len(feature_table)))
    #path_keys = out_prefix + '.keys.dat'
    path_features = out_prefix + '.features.dat'
    print('Writing ' + path_features + ' ...')
    #f1 = open(path_keys, 'w')
    f2 = open(path_features, 'w')
    for k, v in sorted(feature_table.items()):
        #if k.startswith('192168'):
            #f2.write(k + ' ' + ' '.join(list(map(str, v))) + '\n')
        f2.write(k + ' ' + ' '.join(list(map(str, v))) + '\n')

        #f1.write(k + '\n')
        #f2.write(' '.join(list(map(str, v))) + '\n')
    #f1.close()
    f2.close()

in_degrees = gmetrics_lib.Counter()
out_degrees = gmetrics_lib.Counter()
centrality = dict()

#path = '/people/d3m432/tmp/toy.tsv'
#path = '/pic/projects/mnms4graphs/iscx/netflow/testbed-11jun-aggr.tsv'
#flow_path = 'graphs/plogon20120430.dmp.gr'
#transform_eventlog(flow_path)
#flow_path = 'graphs/testbed-13jun-aggr.txt'

# For processing UNB data
#flow_path = sys.argv[1]
#ip_mapper = transform_unb(flow_path)
#prefix = os.path.basename(flow_path)
#prefix = prefix.split('.')[0]
#outdir = '/pic/projects/mnms4graphs/iscx/flo_features'

# For processing simulated TSV files
path_without_tsv_ext = sys.argv[1]
flow_path = path_without_tsv_ext
ip_mapper = process_tsv(flow_path)
prefix = os.path.basename(flow_path)
outdir = '/pic/projects/mnms4graphs/visr/tsv_features'

gmetrics_lib.mkdir_p(outdir)
feature_data_prefix = outdir + '/' + prefix
print('Computing features from : ' + flow_path)
print('Output prefix : ' + feature_data_prefix)

t1 = time.time()
feature_table = dict()
build_feature_table(flow_path, ip_mapper, feature_table, False)
write_feature_matrix(feature_table, feature_data_prefix)
t2 = time.time()
print('Total time taken: ' + str(t2-t1))
