import sys
import os
import numpy as np

#command line arguments:
#1.path to feature matrix files
#2.path to directory where output will be stored
#3.number of roles to be used

feature_matrix_path = sys.argv[1]
out_dir = sys.argv[2]
num_roles = int(sys.argv[3])

#get role definitions

#read in feature matrices
files = os.listdir(feature_matrix_path)
#let the role-mining script do it's thing
#os.system('matlab -nosplash -nodisplay < set_roles({0},{1},{2}) > output.txt'.format(files,feature_matrix_path,num_roles))
#Get role assignments and distribution
distribution = []
for f in files:
    if f.endswith('features.dat') == False:
      continue
    node_by_role = np.loadtxt(feature_matrix_path+f[:-4]+'-node-by-role{}_forcedF.csv'.format(num_roles), delimiter=',')
    node_role = [[line[0], (np.argmax(line[1:])+1)] for line in node_by_role]
    np.savetxt(out_dir+f[:-4]+'_node_assignments.csv', node_role, delimiter=',')
    dist = [0]*num_roles
    for node in node_role:
        dist[node[1] - 1] += 1
    distribution.append([f[:-4]]+dist)

out_file = out_dir+files[0][:-4]+'_role_distribution.csv'
print out_file
np.savetxt(out_file, distribution, delimiter=',', fmt='%s')
