import csv
import numpy as np
import bisect
from operator import itemgetter
import scipy

pref1 = '/home/ubuntu/share_folder/MnMs/ISCX_flo_features/'
pref2 = '/home/ubuntu/share_folder/MnMs/ISCX_Silk/'
feature_files = ['testbed-{}jun.features.dat'.format(i) for i in range(11,18,1)]
edge_files = ['testbed{}jun.txt'.format(i) for i in range(11,18,1)]

for f in range(len(feature_files)):
	#read in existing feature matrices
	feature_matrix = np.loadtxt(pref1+feature_files[f], delimiter=' ',dtype=int)
	#sort matrix by IP
	feature_matrix.sort(key=itemgetter(0))
	#lop off IP column
	features = [:,1:]
	#take transpose of matrix so each row represents the values for one feature
	features = features.T
	#get total number of nodes
	num_nodes = len(features[0])
	#initialize list to store new feature matrix where each value is assigned a bin and changed to a representative value
	binned_features = []
	#using logarithmic binning since feature values tend to follow a power law distribution
	#we're using p = 0.5 thus bin takes bottom half of remaining (sorted values) and assigns current bin value
	p = 0.5
	#define bin boundaries
	bounds = []
	for feature in features:
                #sort the values for each feature
                f = sorted(feature)
                while len(f) > 1:
                        #get index of halfway point of row of values for that feature
                        idx = int(p*len(f))
                        #save as boundary marker
                        bounds.append(f[idx])
                        #lop off bottom half of values
                        f = [idx+1:]
                        #if there's only one value left then we're done here, nothing more to see
                        if len(f) == 1:
                                bounds.append(f[0])
        #create a new list for each feature with bin values instead of actual values
        for feature in feature:
                #initialize list for binned feature values
                new_feature = []
                #find corresponding bin value for each existing feature value and append to new list
                for f in feature:
                        for b in range(len(bounds)):
                                if f <= bounds[b]:
                                        new_feature.append(b)
                                        break
                #add new row for feature to new matrix
                binned_features.append(new_feature)
        #apply transpose to go back to original feature matrix structure
        binned_features = binned_features.T
	#read in edge list
	edges = np.loadtxt(pref2+edge_files[f], delimiter='|', skiprows=1, usecols= (0,1))
	#get list of neighbors for each node
	#compile list of nodes and initialize list
	nodes = [int(row[0]) for row in feature_matrix]
	nodes.sort()
	print nodes[:10]
	#make list for each type of neighbor and a master list of all neighbors
	src_neighbors = [[node] for node in nodes]
	dst_neighbors = [[node] for node in nodes]
	node_neighbors = [[node] for node in nodes]
	#go through edge list and update neighbor lists accordingly
	for edge in edges:
		idx = bisect_left(nodes,int(edge[0]))
		src_neighbors[idx].append(int(edge[1]))
		node_neighbors[idx].append(int(edge[1]))
		idx = bisect_right(nodes,int(edge[1]))
		dst_neighbors[idx].append(int(edge[0]))
		node_neighbors[idx].append(int(edge[0]))
	#remove duplicates
	for i in range(len(nodes)):
                src_neighbors[i] = src_neighbors[i][0] + list(set(src_neighbors[1:]))
                dst_neighbors[i] = dst_neighbors[i][0] + list(set(dst_neighbors[1:]))
                node_neighbors[i] = node_neighbors[i][0] + list(set(node_neighbors[1:]))
	#add recursive features
        s = 0
        rows, cols = binned_features.shape
        #set variable to keep track of when to stop generating features
        #That is, once a set of features are generated where none of the new features are retained because they're too similar to existing features, we stop
        keep_going = True
        #as long as some of the features generated are still being used, keep going
        i = 0
        num_added = 0
        while keep_going:
                #calculate feature value for every node
                for n in range(len(node_neighbors)):
                        #grab feature vector for each of the node's neighbors
                        neighbor_vectors = np.array([np.array(binned_features[bisect_left(nodes,node_neighbors[n][j])][1:]) for j in range(1,len(node_neighbors[n]),1)])
                        #get aggregate and average values for each feature
                        #but only with the features we haven't already done this for
                        #first time through; do for all
                        if i == 0:
                                num_new_features = neighbor_vectors.shape[1]
                        #after that, just newly added
                        else:
                                num_new_features = num_added
                        num_added = 0
                        #calculate sums and averages
                        for c in range(num_new_features):
                                binned_features[n].append(sum(neighbor_vectors[:,-c]))
                                binned_features[n].append(sum(neighbor_vectors[:,-c])/neighbor_vectors.shape[0])
                                #count features added
                                num_added = num_added + 2
                #make rows of each new feature
                new_vectors = binned_features[:,cols:].T
                #initialize list to store vectors that are too similar to existing features
                to_del = []
                #compare each new feature vector to each existing feature vector
                for r in range(new_vectors.shape[0]):
                        for c in range(cols):
                                #get difference between corresponding values in vectors
                                diff = abs(binned_features[:,c] - new_vectors[r])
                                #if the largest difference is smaller than a given threshold then the vector is not different enough to be kept
                                if max(diff) < s:
                                        to_del.append(r)
                #document actual number of new vectors added after weeding out those too similar
                num_added = num_added - len(to_del)
                #if no new vectors were added, we're done here
                if len(to_del) == new_vectors.shape[0]:
                        keep_going = False
                #remove the above identified features that are too similar
                for td in to_del:
                        binned_features = scipy.delete(binned_features,cols+td,1)
                #increment similarity threshold so that the process will eventually stop.
                s = s + 1
                i = i + 1
        #re-add column with IP labels to newly binned and recursively compiled features
        binned_features = np.concatenate((feature_matrix[:,0], binned_features), axis=1)
        #save it because otherwise what are we even doing here
        np.savetxt(pref1+'new_'+feature_files[f], binned_features, delimiter=' ')
                        
        
                        

	

