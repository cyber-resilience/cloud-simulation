#!/usr/bin/python
#import ipaddress
import sys
import os.path
import socket,struct

class IdGenerator:
    def __init__(self):
        self.hashtable = dict()

    def getId(self, item):
        if item in self.hashtable:
            return self.hashtable[item] 
        else:
            id = str(len(self.hashtable))
            self.hashtable[item] = id
            return id

    def count(self):
        return len(self.hashtable)

class Counter:
    def __init__(self):
        self.hashtable = dict()

    def add(self, item):
        if item in self.hashtable:
            self.hashtable[item] += 1
        else:
            self.hashtable[item] = 1

    def elements(self):
        return self.hashtable.items()

def get_quad_addr(decimal_ip):
    packed_value = struct.pack('!I', int(decimal_ip))
    addr = socket.inet_ntoa(packed_value)
    return addr

#unknowns = set()
multiscale_graph = dict()

def update_multiscale_graph(group_id, node_id):
    global multiscale_graph
    if group_id in multiscale_graph:
        group_members = multiscale_graph[group_id]    
        if node_id not in group_members:
            group_members.add(node_id)
    else:
        group_members = set()
        group_members.add(node_id)
        multiscale_graph[group_id] = group_members
   
def store_multiscale_graph(path):
    f = open(path, 'w')
    f.write('[')
    group_list = []
    for group in multiscale_graph:
        group_list.append(group)

    group = group_list[0]
    group_members = list(multiscale_graph[group])
    f.write('[')
    f.write(group_members[0]) 
    for i in range(1, len(group_members)):
        f.write(', ' + group_members[i]) 
    f.write(']')
    
    for j in range(1, len(group_list)):
        group = group_list[j]
        group_members = list(multiscale_graph[group])
        f.write(',[')
        f.write(group_members[0]) 
        for i in range(1, len(group_members)):
            f.write(', ' + group_members[i]) 
        f.write(']')
             
    f.write(']\n')
    f.close() 

def get_group_id(decimal_ip):
    ip_addr = get_quad_addr(decimal_ip)
    if ip_addr == '8.8.8.8':
        return ('s', 'srv_google_dns')
    elif ip_addr == '10.120.0.5':
        return ('s', 'srv_team_portal')
    elif ip_addr == '10.120.0.10':
        return ('s', 'srv_ntp_server')
    elif ip_addr.find('10.110.0.') != -1:
        tokens = ip_addr.split('.')
        return ('s', ('srv_printer_' + tokens[3]))

    tokens = ip_addr.split('.')
    if tokens[0] == '172' and tokens[1] == '16':
        group_id = int(tokens[2])/10
        #return ('t', 't_' + str(group_id))
        #return ('t_' + str(group_id), 't_' + str(group_id))
        return ('t_' + str(group_id), ip_addr)
    elif tokens[0] == '10' and tokens[1] == tokens[2]:
        group_id = int(tokens[2])/10
        #return ('t', 't_' + str(group_id))
        # return ('t_' + str(group_id), 't_' + str(group_id))
        return ('t_' + str(group_id), ip_addr)
    else:
        #unknowns.add(ip_addr)
        #return ('e', ip_addr)
        pos = ip_addr.find('.')
        group_id = 'e_' + ip_addr[0:pos]
        pos = ip_addr.find('.', pos+1)
        node_id = 'e_' + ip_addr[0:pos]
        #return ('e_' + ip_addr[0:pos], 'e')
        return (group_id, node_id)
 
def store_edge(src_group_id, dst_group_id, src_ip, dst_ip):

    if src_group_id < dst_group_id:
        path = 'test/groups/' + src_group_id + '_' + dst_group_id + '.csv'
    else:
        path = 'test/groups/' + dst_group_id + '_' + src_group_id + '.csv'
    
    f = open(path, 'a')
    f.write(src_ip + ',' + dst_ip + '\n')
    f.close()

def collapse_graph():

    path = '/pic/projects/mnms4graphs/nccdc/2013/raw/nccdc_flow_filt1.out'
    f = open(path, 'r')
    groups = Counter()
    edges = set()
    num_edges = 0
    for line in f:
        num_edges += 1
        if len(edges) == 1000000:
            break
        tokens = line.split('|')
        src_ip = tokens[6]
        dst_ip = tokens[7]
        key = src_ip + ',' + dst_ip
        if key not in edges:
            edges.add(key)
        src_group_id = get_group_id(src_ip)
        dst_group_id = get_group_id(dst_ip)
        groups.add(src_group_id[0])
        groups.add(dst_group_id[0])
    f.close()

    list = sorted(groups.elements())
    f = open('/pic/projects/mnms4graphs/nccdc/2013/mods/group_stats.out', 'w')
    for entry in list:
        f.write(entry[0] + ',' + str(entry[1])  + '\n')
    f.close()


def write_summary(path, filter_group, num_nodes, num_nodes_multiscale, num_edges, \
            num_aggregated_netflow_records, num_filtered_netflow_records, \
            num_filtered_edges):

    print('Filter group: ' + filter_group)
    print('Number of nodes in output graph: ' + str(num_nodes))
    print('Number of level-1 nodes in multi-scale graph: ' + str(num_nodes_multiscale))
    print('number of aggregated netflow records: ' + str(num_aggregated_netflow_records))
    print('Number of edges in output graph: ' + str(num_edges))
    print('Number of filtered netflow records: ' + str(num_filtered_netflow_records))
    print('Number of filtered edges from output graph: ' + str(num_filtered_edges))

    f = open(path, 'a')
    f.write(filter_group + ',' + str(num_nodes) + ',' + \
            str(num_nodes_multiscale) + ',' + str(num_edges) + ',' + \
            str(num_aggregated_netflow_records) + ',' + \
            str(num_filtered_netflow_records) + ',' + \
            str(num_filtered_edges) + '\n')
    f.close()

def process_nccdc(filter_group, num_edges_in_graph):

    path = '/pic/projects/mnms4graphs/nccdc/2013/raw/nccdc_flow_filt1.out'
    f = open(path, 'r')
    edges = dict()
    id_gen = IdGenerator()
    group_id_gen = IdGenerator()

    num_aggregated_netflow_records = 0
    num_filtered_netflow_records = 0
    filtered_edges = set()
    REPORTING_INTERVAL = 1000000

    comp_ips = set()
    for line in f:
        tokens = line.split('|')

        num_bytes = float(tokens[3])
        src_ip = tokens[6]
        dst_ip = tokens[7]

        src_group_id = get_group_id(src_ip)
        dst_group_id = get_group_id(dst_ip)

        if src_group_id[0][0] != 'e':
            comp_ips.add(src_group_id[1]) 

        if dst_group_id[0][0] != 'e':
            comp_ips.add(dst_group_id[1]) 

        src_id = id_gen.getId(src_group_id[1])
        dst_id = id_gen.getId(dst_group_id[1])
        edge_key = src_id + ' ' + dst_id

        #if filter_group != '':
            #if filter_group[0] == 'e' or filter_group[0] == 's':
                #if src_group_id[1] == filter_group or \
                    #dst_group_id[1] == filter_group:
                    #num_filtered_netflow_records += 1
                    ##filtered_edges.add(edge_key)
                    #continue
            #else:
                #if src_group_id[0] == filter_group or \
                    #dst_group_id[0] == filter_group:
                    #num_filtered_netflow_records += 1
                    #filtered_edges.add(edge_key)
                    #continue
#
        #src_group_id = group_id_gen.getId(src_group_id[0])
        #dst_group_id = group_id_gen.getId(dst_group_id[0])

        #update_multiscale_graph(src_group_id, src_id)
        #update_multiscale_graph(dst_group_id, dst_id)

        #num_aggregated_netflow_records += 1

        if edge_key in edges:
            edges[edge_key] += num_bytes
        else:
            edges[edge_key] = num_bytes
        
        #if (num_edges % REPORTING_INTERVAL) == 0:
            #print('number of aggregated edges: ' + str(num_edges) + \
                    #' edges in graph: ' + str(len(edges)))
            #print('Number of filtered edges: ' + str(num_filtered_edges))

        if len(edges) == num_edges_in_graph:
            break
    
    f.close()
    print('number of internal ips = ' + str(len(comp_ips)))
    print('number of external ips = ' + str(id_gen.count() - len(comp_ips)))
    sys.exit(0)
        
    if filter_group == '':
        filter_group = 'none'
    outdir = '/pic/projects/mnms4graphs/nccdc/2013/mods'
    dirpath = outdir + '/num_edges-' + str(num_edges_in_graph)
    
    if os.path.isdir(dirpath) == False:
        print('Creating directory: ' + dirpath)
        os.makedirs(dirpath)
    file = dirpath + '/nccdc-filtered-' + filter_group + '.tsv'
    
    print('Writing file: ' + file)
    f_out = open(file, 'w')
    for edge in edges:
        f_out.write(edge + ' ' + str(edges[edge]) + '\n')

    f_out.close()

    partition_file = file + '.partition'
    print('writing partition: ' + partition_file)
    store_multiscale_graph(partition_file)

    summary_file = outdir + '/summary.csv'
    print('Number of nodes in output graph: ' + str(id_gen.count()))

    num_nodes = id_gen.count()
    num_nodes_multiscale = group_id_gen.count()
    num_edges = len(edges)
    num_filtered_edges = len(filtered_edges)

    write_summary(summary_file, filter_group, num_nodes, num_nodes_multiscale, num_edges, \
            num_aggregated_netflow_records, num_filtered_netflow_records, \
            num_filtered_edges)

def process_nccdc_multiscale():

    path = '/pic/projects/mnms4graphs/nccdc/2013/raw/nccdc_flow_filt1.out'
    f = open(path, 'r')
    group_interaction_counter = Counter()
    num_lines = 0
    i = 0

    unknown = 0
    num_ext_traffic = 0
    num_srv_traffic = 0
    num_ext_srv_traffic = 0
    num_srv_ext_traffic = 0
    num_team_ext_traffic = 0
    num_ext_team_traffic = 0
    num_team_srv_traffic = 0
    num_srv_team_traffic = 0
    num_intra_team_traffic = 0
    num_inter_team_traffic = 0

    for line in f:
        num_lines += 1
        tokens = line.split('|')
        src_ip = tokens[6]
        dst_ip = tokens[7]
        src_group = get_group_id(src_ip)
        dst_group = get_group_id(dst_ip)

        src_type = src_group[0]
        dst_type = dst_group[0]
        src_group_id = src_group[1]
        dst_group_id = dst_group[1]

        if num_lines == 1000000:
            break
        if src_type == 't' or dst_type == 't':
            store_edge(src_group_id, dst_group_id, src_ip, dst_ip)
            continue
        else:
            continue

        if src_type != 't' and dst_type != 't':
            if src_type == 'e' and dst_type == 'e':
                num_ext_traffic += 1
            elif src_type == 's' and dst_type == 's':
                num_srv_traffic += 1
            elif src_type == 'e' and dst_type == 's':
                num_ext_srv_traffic += 1
            elif src_type == 's' and dst_type == 'e':
                num_srv_ext_traffic += 1
            else:
                unknown += 1
                print('UNKNOWN src: ' + str(src_type) + ' dst: ' + str(dst_type))
        else:
            if src_type == 't' and dst_type == 'e':
                num_team_ext_traffic += 1
            elif src_type == 'e' and dst_type == 't':
                num_ext_team_traffic += 1
            elif src_type == 't' and dst_type == 's':
                num_team_srv_traffic += 1
            elif src_type == 's' and dst_type == 't':
                num_srv_team_traffic += 1
            elif src_type == 't' and dst_type == 't':
                if src_group_id == dst_group_id:
                    num_intra_team_traffic += 1
                else:
                    num_inter_team_traffic += 1
            else:
                unknown += 1 
                print('UNKNOWN src: ' + str(src_type) + ' dst: ' + str(dst_type))

        #key = src_group_id + ' -- ' + dst_group_id
        #group_interaction_counter.add(key) 
        #num_lines += 1
        test = num_lines % 1000000
        if test == 0:
            print('Processed ' + str(num_lines) + ' lines')
            #print('Number of unknowns = ' + str(len(unknowns)))
            #print('\n\n\n\n\n')
            #fout = open('dots/groups_' + str(i) + '.dot', 'w')
            #fout.write('graph groups {\n')
            #for entry in group_interaction_counter.elements():
                #if entry[1] > 10:
                    #fout.write(entry[0] + ' [weight=' + str(entry[1]) + ']\n')
            #fout.write('}\n')
            #fout.close()

            #fout = open('stats/summary_' + str(i) + '.csv', 'a')
            fout = open('stats/summary.csv', 'a')
            fout.write(str(num_team_srv_traffic + num_srv_team_traffic) + ' ' + \
                str(num_team_ext_traffic + num_ext_team_traffic) + ' ' + \
                str(num_intra_team_traffic) + ' ' + \
                str(num_inter_team_traffic) + ' ' + \
                str(num_ext_srv_traffic + num_srv_ext_traffic) + ' ' + \
                str(num_ext_traffic) + ' ' + str(num_srv_traffic) + '\n')
            fout.close()
                    
            #fout = open('stats/all_' + str(i) + '.csv', 'a')
            fout = open('stats/all.csv', 'a')
            fout.write(str(num_team_srv_traffic) + ' ' + str(num_srv_team_traffic) + ' ' + \
                str(num_team_ext_traffic) + ' ' + str(num_ext_team_traffic) + ' ' + \
                str(num_intra_team_traffic) + ' ' + \
                str(num_inter_team_traffic) + ' ' + \
                str(num_ext_srv_traffic) + ' ' + str(num_srv_ext_traffic) + ' ' + \
                str(num_ext_traffic) + ' ' + str(num_srv_traffic) + '\n') 
            fout.close()
            i += 1
        
    f.close()
    #print('Number of unknowns = ' + str(len(unknowns)))
    #for entry in group_interaction_counter.elements():
        #print(entry[0] + ' [weight=' + str(entry[1]) + ']')

#process_nccdc_multiscale()
if len(sys.argv) == 3:
    filter_group_id = sys.argv[1]
    num_edges_in_graph = int(sys.argv[2])
else:
    filter_group_id = ''
    num_edges_in_graph = 10000

print('Filter group: [' + filter_group_id + ']')
print('Generating graph with ' + str(num_edges_in_graph) + ' edges ...')
process_nccdc(filter_group_id, num_edges_in_graph)

#collapse_graph()

#process_nccdc('srv_google_dns')
#process_nccdc('srv_team_portal')
#process_nccdc('srv_ntp_server')
#process_nccdc('t_0')
#process_nccdc('t_1')
#process_nccdc('t_2')
#process_nccdc('e_10.180')
#process_nccdc('e_74.125')
#process_nccdc('e_192.168')
#process_nccdc('e_10.120')
#process_nccdc('e_128.171')
#process_nccdc('e_10.120')
#process_nccdc('e_74.125')
#process_nccdc('e_192.168')
#process_nccdc('e_74.125')
#process_nccdc('e_192.168')
#process_nccdc('e_74.125')
#process_nccdc('e_192.168')
