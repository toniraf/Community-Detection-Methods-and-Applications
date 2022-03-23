import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import networkx.algorithms.community as nx_com
import numpy as np
import random

# Rgg
# n = 100
# R = 0.3
# f = nx.random_geometric_graph(n, R)

# scale free
# n = 100
# d = 6
# f = nx.barabasi_albert_graph(n, d)

# small world
n = 100
d = 5
p = 0.1
seedno = 5
my = np.random.RandomState(seedno)
f = nx.watts_strogatz_graph(n, d, p, my)

print(nx.is_connected(f))
c = greedy_modularity_communities(f)
mod = nx_com.modularity(f, c)
print("Number of communities: ", len(c))
print("Modularity :", mod)

# save graph to txt file
df = list(f.edges())
print(len(df))
np.savetxt("smw6.csv", df, delimiter=",", fmt='%s')