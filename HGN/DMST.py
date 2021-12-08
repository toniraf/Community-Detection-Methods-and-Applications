import sys
import networkx as nx
import numpy as np
import random 

def dmst(G,t):
    
    G2 = nx.Graph()
    for _ in range(t):
        minimum_sp_tree = nx.minimum_spanning_tree(G)
        for edge in list(minimum_sp_tree.edges()):
            G2.add_edge(edge[0],edge[1])
            G.remove_edge(edge[0],edge[1])
    
    return(G2)


if __name__ == "__main__":
    number_nodes = int(sys.argv[1])
    pos = {i: (random.random(), random.random()) for i in range(number_nodes)}

    distances = np.empty((number_nodes,number_nodes))
    for i in range(number_nodes):
        for j in range(0,2):
            distances[i][j] = np.sqrt( (pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2)

    G = nx.random_geometric_graph(number_nodes, 1.5, 2, pos)
    for edge in list(G.edges()):
        G[edge[0]][edge[1]]['weight'] = distances[edge[0]][edge[1]]
    print("Number of edges in graph: ", len(G.edges()))
    dmst_graph = dmst(G,5)
    print("Number of edges in DMST graph: ", len(dmst_graph.edges()))
