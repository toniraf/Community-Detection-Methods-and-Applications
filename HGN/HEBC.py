import numpy as np
import networkx as nx
import math
import sys
import random
# import save_load as sl
import HGN
import DMST as dmst
import embed


# np.seterr(over='ignore')

def hyperbolic_edge_centrality(G, coordinatesMatrix, src):
    coordinatesMatrix = np.delete(coordinatesMatrix, 0, 1)
    edges_number = len(G.edges())

    # here we need the dimensions of the embedding, this can be read from a configuration file 

    dim = np.shape(coordinatesMatrix)[1]

    # here we need this array because at the end it contains the scores achieved
    # HEBC =  np.zeros((edges_number,3))

    nodes_number = len(G.nodes())

    # tmp = [G.degree()[i] for i in range(nodes_number)]
    tmp = [G.degree()[i] for i in range(nodes_number) if G.has_node(i)]
    pSize = max(tmp)
    # testMatrix = np.zeros((nodes_number,pSize))

    indexMatrix = [0] * nodes_number

    # tempArray is a list now
    testMatrix = []
    for i in range(0, nodes_number):
        if G.has_node(i):
            tempArray = list(G.neighbors(i))
            tempArray.sort()
            testMatrix.append(tempArray)
            # print(tempArray)
            # for j in range(len(tempArray)):
            #    testMatrix[i][j] = tempArray[j]
            indexMatrix[i] = len(tempArray)

    temp = np.zeros((edges_number, 3))
    # np.savetxt("testMatrix.txt",testMatrix)
    k = 0
    edge_dict = dict()
    for edge in list(G.edges()):
        temp[k][0] = edge[0]
        temp[k][1] = edge[1]
        edge_dict[str(edge[0]) + ' ' + str(edge[1])] = k
        edge_dict[str(edge[1]) + ' ' + str(edge[0])] = k
        k = k + 1
    # maybe i can turn this into a list

    P = np.zeros((nodes_number, nodes_number))
    for destination in range(src):
        indexP = [0] * nodes_number
        sigma = [0] * nodes_number
        sigma[destination] = 1
        distances = [0] * nodes_number
        # P = np.zeros((nodes_number, nodes_number))
        # STAGE 1 - Topological Sort

        # access to database for this information might be needed
        dst = coordinatesMatrix[destination][:]

        # a faster way to calculate nodes distance

        ysum = 1
        for j in range(0, dim):
            ysum += dst[j] ** 2

        for vertex in range(nodes_number):
            xsum = 1
            xysum = 0

            for j in range(1, dim):
                # access to database for this information might be needed
                xsum += coordinatesMatrix[vertex][j] ** 2
                xysum += coordinatesMatrix[vertex][j] * dst[j]
            t = np.sqrt(ysum * xsum, dtype=np.float64) - xysum
            # t = np.array(math.sqrt(ysum*xsum))-xysum
            if (t < 1):
                t = 1.0
            dist = math.acosh(t)

            distances[vertex] = dist
        # distances = list(distances)
        DAG = list(np.argsort(distances))
        DAG.reverse()
        np.savetxt('distances', distances)
        # Part 2 - number of greedy pths between nodes and destination

        for i in range(nodes_number - 1, -1, -1):
            if G.has_node(i):
                v = DAG[i]
                for j in range(int(indexMatrix[v])):
                    try:
                        w = int(testMatrix[v][j])
                        if distances[w] > (distances[v] + 0.3):
                            sigma[w] += sigma[v]
                            indexP[w] += 1
                            P[w][int(indexP[w]) - 1] = v
                    except IndexError:
                        print("out of range")
        # Part 3 
        delta = [0] * nodes_number
        # print(edge_dict)
        # S returns vertices in order of non-increasing distance from s
        for node in range(nodes_number):
            if G.has_node(node):
                # pop w<-S
                w = DAG[node]
                if sigma[w] > 0:
                    for j in range(int(indexP[w])):
                        v = int(P[w][j])
                        c = (sigma[v] / sigma[w]) * (1 + delta[w])
                        pointer = edge_dict[str(w) + ' ' + str(v)]
                        temp[pointer][2] += c
                        # temp[w][v]+=c
                        # temp[v][w]+=c
                        delta[v] += c

    # k = 0
    # np.savetxt('temp',temp)
    # here we just form a matrix containing the values
    # we may store the values to a database
    # for edge in G.edges():
    #        
    #    HEBC[k][0] = edge[0]
    #    HEBC[k][1] = edge[1]
    #    HEBC[k][2] = temp[edge[0]][edge[1]]
    #    k+=1

    # sorted so that the most central edges appear first
    temp = temp[temp[:, 2].argsort()][::-1]
    # np.savetxt('HEBC.txt',HEBC)
    return (temp)


if __name__ == '__main__':
    o = 'outputs'
    # cols = tuple([i for i in range(2+1)])
    # number_nodes = int(sys.argv[1])
    # G = nx.scale_free_graph(number_nodes)
    # G = G.to_undirected()
    # G2 = nx.Graph(G)

    # src = int(sys.argv[2])
    e = -1
    l = 'testingdist.txt'
    r = 'testinglands.txt'
    t = 'testing'
    filename = 'datasets/outliers.txt'
    L = 6
    b = 6
    i = 6
    u = 600
    x = 2
    G = HGN.getFullgraph(filename)
    G = dmst.dmst(G, 5)
    coordinatesMatrix = embed.embed(G, o, l, b, x, t, r, u, e, L, i)
    np.savetxt('coords.txt', coordinatesMatrix)
    # coordinatesMatrix = np.loadtxt('coords')
    # G = sl.load('net.json')
    adjacency_matrix = nx.adjacency_matrix(G, nodelist=sorted(list(G.nodes())))
    adjacency_matrix = adjacency_matrix.todense()
    np.savetxt('adjacency_matrix', adjacency_matrix)
    HEBC = hyperbolic_edge_centrality(G, coordinatesMatrix, 600)
    print(HEBC)
