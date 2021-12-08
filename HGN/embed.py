import sys
import numpy as np
import networkx as nx
# import random
# import subprocess
import os

import landmarkSelect as lands


def embed(G, o, l, b, x, t, r, u, e, L, i):
    lands.select_landmarks(G, 'testing', L)

    print("o: ", o)
    print("l: ", l)
    print("b: ", b)
    print("x: ", x)
    print("t: ", t)
    print("r: ", r)
    print("u: ", u)
    print("e: ", e)
    print("L: ", L)
    print("i: ", i)
    cmd = "./rigel -b " + str(L) + " -e -1 -i " + str(i) + " -L " + str(
        L) + " -l " + l + " -o " + o + " -r " + r + " -t " + t + " -u " + str(u) + " -x " + str(x) + " -y -1"
    os.system(cmd)
    cmd = "./rigel -b " + str(L) + " -e -1 -i " + str(i) + " -L " + str(
        L) + " -l " + l + " -o " + o + " -r " + r + " -t " + t + " -u " + str(u) + " -x " + str(x) + " -y 0"
    os.system(cmd)
    cols = tuple([i for i in range(x + 1)])
    land_coords = np.loadtxt(o + ".land", dtype='float64', delimiter=' ', usecols=cols)
    node_coords = np.loadtxt(o + "0.coord", dtype='float64', delimiter=' ', usecols=cols)

    # coordinates Matrix: every row [id dim1 dim2 ... dimN]
    coordinatesMatrix = np.concatenate((land_coords, node_coords))
    coordinatesMatrix = coordinatesMatrix[coordinatesMatrix[:, 0].argsort()]
    return (coordinatesMatrix)


if __name__ == "__main__":
    number_nodes = int(sys.argv[1])
    o = 'outputs'
    b = 5
    e = -1
    i = 5
    L = 5
    l = 'testingdist.txt'
    r = 'testinglands.txt'
    t = 'testing'
    u = number_nodes
    x = 2
    y = 0
    G = nx.scale_free_graph(number_nodes)
    G = G.to_undirected()
    embed(G, o, l, b, x, t, r, u, e, L, i)
