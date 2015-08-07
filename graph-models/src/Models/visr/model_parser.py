#!/usr/bin/python
import sys
from ontology_reader import Model
from network_builder import NetworkBuilder

def print_edge(src, relation, target):
  print(src + ' -> ' + target)
  
class Node:
  def __init__(self, class_id, node_id):
    self.class_id = class_id
    self.node_id = node_id
    self.entity_type = 'Node'
  
  def get_class_id(self):
    return self.class_id

  def get_node_id(self):
    return self.node_id

  def get_entity_type(self):
    return self.entity_type

class NodeGroup:
  def __init__(self, class_id, node_id, group_sz):
    self.class_id = class_id
    self.node_id = node_id
    self.group_size = int(group_sz)
    self.entity_type = 'NodeGroup'

  def get_class_id(self):
    return self.class_id

  def get_node_id(self):
    return self.node_id

  def get_entity_type(self):
    return self.entity_type

  def get_members(self):
    members = []
    for i in range(self.group_size):
      u = self.node_id + '_' + str(i)
      members.append(u)
    return members
    
  def expand_actions(self, action_to, other, relation):
    for i in range(self.group_size):
      u = self.node_id + '_' + str(i)
      if action_to:
        print_edge(u, relation, other.get_node_id())
      else:
        print_edge(other.get_node_id(), relation, u)

class Action:
  def __init__(self, s, t, r):
    self.src = s
    self.target = t
    self.relation = r
  
  def get_src(self):
    return self.src

  def get_target(self):
    return self.target

  def get_relation(self):
    return self.relation

class Enterprise:
  def __init__(self, path):
    self.model = Model("ontology.graph")
    self.nodes = dict()
    self.actions = []
    self.network = NetworkBuilder()

    f = open(path)
    for line in f:
      if line[0] == '#':
        continue
      tokens = line.strip().split(' ')
      if len(tokens) < 3:
        continue
      if tokens[1] == 'type':
        class_name = self.model.get_class_info(tokens[-1])
        if class_name == 'N/A':
          print('UNKNOWN CLASS : ' + tokens[-1])
          continue
        else:
          node = Node(tokens[-1], tokens[0])
          self.nodes[tokens[0]] = node
      elif tokens[1] == 'isGroupOf':
        node_grp = NodeGroup(tokens[2], tokens[0], tokens[4])
        self.nodes[tokens[0]] = node_grp
      elif tokens[1] == 'uses':
        action = Action(tokens[0], tokens[2], tokens[4])
        self.actions.append(action)
      elif tokens[1] == 'networkType':
        self.network.build(tokens)
      elif tokens[1] == 'attachTo':
        attach_src = tokens[0]
        if attach_src in self.nodes:
          src = self.nodes[attach_src]
          if src.get_entity_type() == 'NodeGroup':
            members = src.get_members()
            for member in members:
              new_tokens = tokens
              new_tokens[0] = member
              self.network.build(new_tokens)
          else:
            self.network.build(tokens)
        else:
          self.network.build(tokens)
    f.close()

  def get_entity_type(self, entity_name):
    return self.nodes[entity_name].get_entity_type() 

  def print_app_graph(self):
    #for (k,node) in self.nodes.iteritems():
      #qname = self.model.get_class_info(node.get_class_id())
      #node_id = node.get_node_id()
      #print('--- ' + node.get_entity_type())
      #print(qname + ',' + node_id)
    print('digraph dataflow {') 
    for a in self.actions:
      src = self.nodes[a.get_src()]
      target = self.nodes[a.get_target()]
      relation = a.get_relation()
      if src.get_entity_type() == 'NodeGroup':
        src.expand_actions(True, target, relation)
      elif target.get_entity_type() == 'NodeGroup':
        target.expand_actions(False, src, relation)
      else:
        print_edge(a.get_src(), relation, a.get_target())
      if a.get_src() == 'SalesTeam_0':
        print(a.get_src() + '#############' +  a.get_target())
    print('}')

  def print_topology(self):
    print('graph topology {')
    self.network.print_topology()
    print('}')
  
e = Enterprise(sys.argv[1])
e.print_app_graph()
#e.print_topology()
