import sys
import numpy as np
import networkx as nx
import random

def select_landmarks(G,filename,num_landmarks):

    # we need to find nodes of maximum degree here 
    nodes_number = len(G.nodes())
    tmp = [G.degree()[n] for n in list(G.nodes())]

    inds = list(np.argsort(tmp))
    inds.reverse()
    landmarks = [inds[i] for i in range(num_landmarks)]


    # make the necessary files for rigel embedding
    f = open(filename+'dist.txt','w')
    for land in landmarks:
        for node in range(nodes_number):
            # here we may use a database in order to compute the shortest path length
            try:
                if G.has_node(land) and G.has_node(node):
                    dst = nx.shortest_path_length(G, source=land, target=node)
            except nx.NetworkXNoPath:
                dst = 1000
            f.write(str(dst) + ' ')
        f.write('\n')
    f.close()

    f = open(filename+'lands.txt','w')
    for land in landmarks:
        f.write(str(land)+'\n')
    f.close()

    f = open(filename+'.num','w')
    f.write('0 '+str(nodes_number))
    f.close()

    f = open(filename+'0.ord','w')
    for i in range(nodes_number):
        if i not in landmarks:
            f.write(str(i)+'\n')
    f.close()

    return(landmarks)


if __name__ == "__main__":
    number_nodes = int(sys.argv[1])
    number_landmarks = int(sys.argv[2])
    pos = {i: (random.random(), random.random()) for i in range(number_nodes)}

    G = nx.random_geometric_graph(number_nodes, 0.4, 2, pos)

    landmarks = select_landmarks(G,'testing',number_landmarks)
    print(landmarks)