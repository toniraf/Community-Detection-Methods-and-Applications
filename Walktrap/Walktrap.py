import networkx as nx
import matplotlib.pyplot as plt
import random
import igraph
from igraph import *

filename = sys.argv[1]
# G = nx.read_edgelist(filename, nodetype=int)
f = Graph.Read_Edgelist(filename, directed = False)
# print(f)
v = f.community_walktrap()
clusters = v.as_clustering()
print(clusters)

