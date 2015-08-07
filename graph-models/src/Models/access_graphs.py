#!/usr/bin/env python3
import sys
sys.path.append('../Metrics/')
import flow_lib
import os

class AccessControlGraph:
  def __init__(self):

  def add_access(self, appl, host, user):
    return

  def change_credentials(self, appl, host, user):
    return

  def access_resource(self, appl, host, user):
    return

  def export_access_control(self, out_path):
    return

  def export_access_activity(self, out_path):
    return

class AccessControlGraphBuilder:
    def __init__(self):
        self.host_user_map = dict()
        self.sep = ','
        return

    def transform(self, flow):
        src_ip = flow.get_ip(True)
        user = flow.get_user()

        if src_ip not in self.host_user_map:
            self.host_user_map[src_ip] = set()
        self.host_user_map[src_ip].add(user)
        return

    def store(self, outpath):
        edge_map = dict()
        users = set()
        sep = self.sep
        id_mapper = flow_lib.HashedIdMapper()
        for host in self.host_user_map.keys():
            user_set = sorted(list(self.host_user_map[host]))
            for u in user_set:
                users.add(u)
            num_users = len(user_set)
            for i in range(num_users-1):
                for j in range(i+1, num_users):
                    u = id_mapper.map(user_set[i])
                    v = id_mapper.map(user_set[j])
                    if u < v:
                        key = u + sep + v
                    else:
                        key = v + sep + u
                    if key not in edge_map:
                        edge_map[key] = 1
                    else:
                        edge_map[key] += 1
                    #print(user_set[i] + ' -- ' + user_set[j]) 
        print('# edges = ' + str(len(edge_map)))
        print('# users = ' + str(len(users)))

        f_out = open(outpath, 'w')
        for k in edge_map.keys():
            #f_out.write(k + ' ' + str(edge_map[k]) + '\n')
            f_out.write(k + '\n')
        f_out.close()
        return 
    
def build_access_control_graphs(raw_dir, out_dir):
    files = os.listdir(raw_dir)
    for f in files:
        if f.endswith('.dmp.gr')
            raw_path = dirpath + '/' + f
            graph_builder = AccessControlGraphBuilder()
            flow_lib.process_flow_data(raw_path, flow_lib.parse_event_log, 
                    graph_builder.transform)
            out_file = os.path.basename(raw_path) 
            out_path = out_dir + '/' + out_file + '.csv'
            graph_builder.store(out_path)

def build_access_control_graph(raw_path):
    graph_builder = AccessControlGraphBuilder()
    flow_lib.process_flow_data(raw_path, flow_lib.parse_event_log, 
            graph_builder.transform)
    out_dir = '/Users/d3m432/tmp'
    out_file = os.path.basename(raw_path) 
    out_path = out_dir + '/' + out_file + '.csv'
    graph_builder.store(out_path)


raw_path = '/Users/d3m432/data/arc/plogon20120307.dmp.gr'
build_access_control_graph(raw_path)
