import sys
import numpy as np
import networkx as nx
import random
# import subprocess
#import os
import embed
import HEBC
import save_load as sl
#import DMST as dmst
from scipy.spatial import distance
#import matplotlib
from networkx.algorithms.community.quality import modularity


def getFullgraph(filename):
    positions = np.loadtxt(filename)
    # positions = np.delete(positions,2,1)
    G = nx.Graph()
    for i in range(len(positions)):
        for j in range(len(positions)):
            dist = distance.euclidean(positions[i], positions[j])
            G.add_edge(i, j, weight=dist)
    # nx.draw_networkx(G)
    return (G)


def largest_conn_comp(G):
    # graphs = list(nx.connected_component_subgraphs(G))
    graphs = list(G.subgraph(c) for c in nx.connected_components(G))
    lc = 0
    max_cc = 0
    for gr in range(len(graphs)):
        siz = len(graphs[gr].nodes())
        if (siz > max_cc):
            max_cc = siz
            lc = gr
    G2 = graphs[lc]
    return (G2)


def smallest_conn_comp(G):
    # graphs = list(nx.connected_component_subgraphs(G))
    graphs = list(G.subgraph(c) for c in nx.connected_components(G))
    sc = 0
    min_cc = 10000000
    for gr in range(len(graphs)):
        siz = len(graphs[gr].nodes())
        if (siz < min_cc):
            min_cc = siz
            sc = gr
    G2 = graphs[sc]
    return (G2)


def community_discovery(G, k, batchSize, o, l, x, t, r, e):
    # Inputs:
    #           adj: the adjacency matrix of the graph
    #           k: the required number of communities
    #           batchSize: the size of the Batch (up to how many edges will be
    #           removed before a new embedding)
    #           The next parameters are used for the rigel embedding
    #           o: path for the output file
    #           l: path for the Dist file
    #           x: the number of dimensions
    #           t: input file path
    #           r: path for the landmarks file
    #           e: curvature of hyperbolic space
    # Outputs:
    #           modules: cell array 1 x k . Each cell contains the nodes of the
    #           corresponding module.

    communities_discovered = 1
    print("G IS directed?", G.is_directed())
    modules_found = []
    mapping = {i: i for i in range(len(G.nodes()))}
    # G = max(nx.connected_component_subgraphs(G), key=len)
    # G_largest.add_edges_from(list(G.edges()))
    H = nx.Graph()
    H.add_nodes_from(list(G.nodes()))
    H.add_edges_from(G.edges())
    modules_found = [list(G.nodes())]
    lm = list(G.nodes())
    while (communities_discovered <= k):
        L = 16
        b = 16
        i = 16
        u = len(G.nodes())
        # print("Is G connected?", nx.is_connected(G))
        coordinatesMatrix = embed.embed(G, o, l, b, x, t, r, u, e, L, i)
        np.savetxt('coords', coordinatesMatrix)
        w = HEBC.hyperbolic_edge_centrality(G, coordinatesMatrix, len(G.nodes()))

        p = 0

        while (p < batchSize) and nx.is_connected(G):
            # while (p<batchSize) and (nx.number_connected_components(G)==communities_discovered):
            print("hi")
            G.remove_edge(w[p][0], w[p][1])
            edge0 = mapping[w[p][0]]
            edge1 = mapping[w[p][1]]
            H.remove_edge(edge0, edge1)
            p += 1

        # if (nx.number_connected_components(G) != communities_discovered):
        if not nx.is_connected(G):
            print("found community")
            modules_found.remove(lm)
            communities_discovered += 1
            print("communities found")
            G2 = smallest_conn_comp(G)
            translation = []
            for nn in list(G2.nodes()):
                nodeID = mapping[nn]
                translation.append(nodeID)
            modules_found.append(translation)

            G3 = largest_conn_comp(G)
            translation = []
            for nn in list(G3.nodes()):
                nodeID = mapping[nn]
                translation.append(nodeID)
            modules_found.append(translation)
            max_siz = 0
            lm = []
            for mod in modules_found:
                if len(mod) > max_siz:
                    max_siz = len(mod)
                    lm = mod

            del mapping
            kk = 0
            mapping = dict()
            for i in lm:
                mapping[kk] = i
                kk += 1
            # print(mapping)
            G = H.subgraph(lm)
            inv_map = {v: k for k, v in mapping.items()}
            G = nx.relabel_nodes(G, inv_map)
            print(len(lm))
    # modules_found = nx.connected_components(G)
    return (modules_found)


if __name__ == "__main__":

    filename = sys.argv[1]
    k = int(sys.argv[2])
    batchSize = int(sys.argv[3])
    x = int(sys.argv[4])

    # read graph from file to db

    # G = getFullgraph(filename)
    # G = dmst.dmst(G,5)

    # number_nodes = int(sys.argv[1])
    # G = nx.scale_free_graph(number_nodes)
    # G = G.to_undirected()
    # G = nx.Graph(G)

    # G.remove_nodes_from(nx.isolates(G))
    # tmp = list(G.nodes())
    # mapping = {tmp[i]:i for i in range(len(tmp))}
    # G = nx.relabel_nodes(G,mapping)

    # adjacency matrix is symmetric
    G = nx.read_edgelist(filename, nodetype=int)
    # G.remove_edges_from(G.selfloop_edges())
    G.remove_edges_from(nx.selfloop_edges(G))
    print(G.nodes())
    if not nx.is_connected(G):
        iso_list = list(nx.isolates(G))
        # num of components - C
        for i in iso_list:
            target = random.choice(list(G.nodes()))
            G.add_edge(i, target)

    adj_matrix = nx.adjacency_matrix(G)
    adj_matrix = adj_matrix.todense()
    np.savetxt('my_matrix', adj_matrix)
    sl.save(G, 'net.json')
    o = 'outputs'
    e = -1
    l = 'testingdist.txt'
    r = 'testinglands.txt'
    t = 'testing'
    modules = community_discovery(G, k - 1, batchSize, o, l, x, t, r, e)

    # np.savetxt('communities.txt', modules)
    # a = nx.connected_component_subgraphs(G)
    modules2 = []
    for m in modules:
        # print(len(m.nodes()))
        m.sort()
        modules2.append(m)
        # if len(m)==k:
        #    print(m)
    print(modules)
    print("modularity:", modularity(G, modules))
