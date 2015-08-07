#!/usr/bin/python
import sys
#from flow_lib import HashedIdMapper

class HashedIdMapper:
    def __init__(self, offset=0):
        self.id_map = dict()
        self.rev_mapping = dict()
        self.offset = offset

    #def load(self, csv_file):
        #fin = open(csv_file)
        #for line in fin:
            #t = line.strip().split(',')
            #self.id_map[t[0]] = t[1]
        #fin.close()
#
    #def reset(self):
        #self.id_map.clear()
    
    def map(self, key):
        if key in self.id_map:
            id = self.id_map[key]
        else:
            id = str(self.offset + len(self.id_map))
            self.id_map[key] = id
            self.rev_mapping[id] = key 
        return id
    
    def rev_map(self, id):
        if id not in self.rev_mapping:
            return ''
        return self.rev_mapping[id]

    def store(self, outpath):
        fout = open(outpath, 'w')
        for k,v in self.id_map.items():
            fout.write(k + ',' + v + '\n')
        fout.close()

def dot2tsv(dot_path):
  outpath = dot_path.replace('.dot', '.tsv')
  f = open(dot_path)
  f_out = open(outpath, 'w')
  id_mapper = HashedIdMapper()
  for line in f:
    if line.find('--') == -1 and line.find('->') == -1:
      continue
    tokens = line.strip().split(' ')
    u = id_mapper.map(tokens[0])
    v = id_mapper.map(tokens[2])
    f_out.write(u + ' ' + v + '\n')
  f.close()
  f_out.close()
  map_path = outpath + '.map'
  id_mapper.store(map_path)

dot2tsv(sys.argv[1])
