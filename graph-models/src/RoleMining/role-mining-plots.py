from matplotlib import pyplot as plt
import numpy as np
import prettyplotlib as ppl
import os
import sys
import string
import itertools

#script is passed the directory where the role distribution files can be found
path = sys.argv[1]
num_roles = int(sys.argv[2])
files = os.listdir(path)

for f in files:
	if '_role_distribution' in f:
		dists = np.loadtxt(path+f, delimiter=',', usecols=(range(1,num_roles+1)))
		labels = list(np.loadtxt(path+f, delimiter=',', usecols=(0,), dtype=str))
		fig, ax = plt.subplots(nrows=1,ncols=len(labels),sharey=True,figsize=(16,8))
		fig.text(0.5, 0.04, 'Role', ha='center')
		fig.text(0.04, 0.5, 'Number of Nodes', va='center', rotation='vertical')
		ax = ax.ravel()
		idx = 0
		for d in dists:
			d = [int(i) for i in d]
			ppl.bar(ax[idx],np.arange(num_roles),d,annotate=True,xticklabels=string.uppercase[:num_roles])
			ax[idx].set_title(labels[idx])
			idx += 1
		plt.savefig(f[:-4] + '_' + str(num_roles) + '_role_dist.png')
