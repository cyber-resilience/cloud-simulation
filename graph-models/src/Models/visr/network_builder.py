#!/usr/bin/python
import random

def print_link(u, v, link_type):
  print(u + ' -- ' + v)

class HubNetwork:
  def __init__(self, name):
    self.size = 10 #int(size)
    self.name = name
    self.linked_to = 'NONE'
    self.attach_list = []
    self.network_type = 'Hub'

  def get_network_type(self):
    return self.network_type

  def attach(self, edge_device): 
    self.attach_list.append(edge_device)

  def print_network(self):
    hub = self.name #+ '_router'
    if len(self.attach_list) > 0:
      for u in self.attach_list:
        print_link(hub, u, 'edge_link')
    else:
      for i in range(self.size):
        u = self.name + '_' + str(i)
        print_link(hub, u, 'edge_link')
    #if self.other != 'NONE':
      #print_link(hub, self.other, 'backbone')

class CoreNetwork:
  def __init__(self, name, N):
    self.name = name
    self.num_planes = 2
    self.plane_sizes = [N, N]
    self.attach_list = []
    self.network_type = 'Core'

  def get_network_type(self):
    return self.network_type

  def attach(self, edge_device):
    self.attach_list.append(edge_device)

  def attach_core(self, other, n):
    ids = other.get_interface_ids(n)
    for u in ids:
      self.attach(u)

  def get_interface_ids(self, n):
    plane_size = self.plane_sizes[0]
    ids = []
    for i in range(n):
      interface_node_id = self.name + '_p0_' + str(random.randint(0, plane_size-1))
      ids.append(interface_node_id)
    return ids

  def print_network(self):
    plane_size = self.plane_sizes[0]
    next_switch = 0
    for edge_device in self.attach_list:
      u = self.name + '_p0_' + str(next_switch % plane_size)
      print_link(u, edge_device, 'edge_link')
      next_switch += 1

    for i in range(self.num_planes-1):
      plane_a = []
      plane_b = []
      for j in range(self.plane_sizes[i]):
        u = self.name + '_p' + str(i) + '_' + str(j)
        plane_a.append(u)
      for j in range(self.plane_sizes[i+1]):
        v = self.name + '_p' + str(i+1) + '_' + str(j)
        plane_b.append(v)
      for u in plane_a:
        for v in plane_b:
          print_link(u, v, 'core')

class NetworkBuilder:
  def __init__(self):
    self.components = dict()

  def build(self, tokens):
    if tokens[1] == 'networkType':
      self.add_component(tokens)
    elif tokens[1] == 'attachTo':
      self.add_link(tokens) 

  def add_component(self, tokens):
    comp_name = tokens[0]
    comp_type = tokens[-1]
    if comp_type == 'Hub':
      #print('Creating Hub = ' + comp_name)
      self.components[comp_name] = HubNetwork(comp_name)
    elif comp_type.find('CoreNetwork') != -1:
      #print('Creating CoreNetwork')
      parts = comp_type.split('-')
      if len(parts) > 1:
        plane_size = int(parts[-1])
      else:
        plane_size = 4
      self.components[comp_name] = CoreNetwork(comp_name, plane_size)

  def add_link(self, tokens):
    peripheral_id = tokens[0]
    core = tokens[2]
    if core not in self.components:
      print('UNKNOWN NETWORK COMPONENT: ' + core)
      return
    core_comp = self.components[core]

    if peripheral_id in self.components:
      peripheral_comp = self.components[peripheral_id]
      if peripheral_comp.get_network_type() == 'Core': 
        core_comp.attach_core(peripheral_comp, 2)
      else:
        core_comp.attach(peripheral_id)
    else:
      core_comp.attach(peripheral_id)

  def print_topology(self):
    for (name,comp) in self.components.iteritems():
      comp.print_network()
