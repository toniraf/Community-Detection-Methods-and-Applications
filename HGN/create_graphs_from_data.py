import sys
import numpy as np
import networkx as nx
from scipy.spatial import distance 
import DMST as dmst

if __name__ == '__main__':
	filename = sys.argv[1]
	graph_filename = sys.argv[2]
	f = open(filename, 'r')
	print("hi")
	positions = np.loadtxt(filename)
	G = nx.Graph()
	for i in range(len(positions)):
		for j in range(i, len(positions)):
			dist = distance.euclidean(positions[i],positions[j])
			G.add_edge(i,j,weight=dist)
	G = dmst.dmst(G,5)
	f2 = open(graph_filename,'w')
	for edge in list(G.edges()):
		f2.write(str(edge[0]) + ' ' + str(edge[1]) + '\n')
	
	f.close()
	f2.close()

	
