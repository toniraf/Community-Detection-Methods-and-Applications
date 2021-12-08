import simplejson as json
import networkx as nx


def save(G, fname):
    json.dump(dict(nodes=[[n, G.nodes[n]] for n in G.nodes()],
                   edges=[ [ i[0], i[1], G.edges[i] ] for i in list(G.edges()) ] ),
              open(fname, 'w'), indent=2)


def load(fname):
    G = nx.DiGraph()
    d = json.load(open(fname))
    G.add_nodes_from(d['nodes'])
    G.add_edges_from(d['edges'])
    return G