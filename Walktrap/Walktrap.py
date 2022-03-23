import sys
import time

start_time = time.time()
import networkx as nx
# import matplotlib.pyplot as plt
# import random
import igraph
from sklearn.metrics.cluster import normalized_mutual_info_score
from igraph import *

# ---- Real Datasets ----- #
filename = sys.argv[1]
groundfile = sys.argv[2]
# G = nx.read_edgelist(filename, nodetype=int)
f = Graph.Read_Edgelist(filename, directed=False)
# g = f.to_networkx()
# print(nx.is_connected(g))
v = f.community_walktrap()
clusters = v.as_clustering()
print(clusters.modularity)
# pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
# f.vs['color']=pal.get_many(clusters.membership)
# igraph.plot(f)

# --------NMI calculation --------#

with open(groundfile) as file:
    lines = [line.rstrip() for line in file]

groundl = list(map(int, lines))
#NMI = compare_communities(clusters.membership, groundl, method="nmi")

NMI = normalized_mutual_info_score(groundl, clusters.membership)
print("NMI:", NMI)
print("--- %s seconds ---" % (time.time() - start_time))

# ------- RGG model ------ #
# n = 100
# R = 0.2
# f = nx.random_geometric_graph(n, R)
# g = igraph.Graph(directed=True)
# g.add_vertices(f.nodes())
# g.add_edges(f.edges())
# v = g.community_walktrap()
# clusters = v.as_clustering()
# print(clusters.modularity)
# pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
# g.vs['color'] = pal.get_many(clusters.membership)
# igraph.plot(g)
