#!/usr/bin/python

class Model:
  def __init__(self, path):
    self.class_tree = dict()
    self.class_tree['ROOT'] = set()
    f = open(path)
    for line in f:
      tokens = line.strip().split(' ')
      if len(tokens) < 3:
        continue
      if tokens[1] == 'isA':
        parent = tokens[2]
        child = tokens[0]
        if parent == 'BasicConcept':
          self.class_tree['ROOT'].add(child)
        else:
          if parent not in self.class_tree:
            self.class_tree[parent] = set()
          self.class_tree[parent].add(child)
    f.close() 
    self.expand_paths()

  def expand_paths(self):
    visited = set()
    visit_queue = []
    visit_queue.append('ROOT')
    self.qnames = dict()
    while len(visit_queue) > 0:
      parent_qname = visit_queue.pop(0) 
      tokens = parent_qname.split(':')
      parent = tokens[-1]
      if parent not in self.class_tree:
        continue
      children = self.class_tree[parent]
      for c in children:
        if c not in visited:
          if parent_qname == 'ROOT':
            c_qname = c
          else:
            c_qname = parent_qname + ':' + c
          self.qnames[c] = c_qname
          visit_queue.append(c_qname)
      visited.add(parent)

  def get_class_info(self, name):
    if name in self.qnames:
      return self.qnames[name]
    else:
      return 'N/A'

#model = Model("ontology.graph")
#print(model.get_class_info("SharePointServer"))
