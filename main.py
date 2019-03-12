import networkx as nx
import matplotlib.pyplot as plt
import random
from statistics import median
import pandas as pd
from math import inf


def giant_comp(g):
    return max(nx.connected_component_subgraphs(g), key=len)


def create_random_graph(n, p):
    g = nx.fast_gnp_random_graph(n, p)
    return giant_comp(g)


def create_scale_free_graph(n):
    g = nx.scale_free_graph(n)
    return nx.Graph(g)


def create_ex_graph():
    g = nx.Graph()
    g.add_edge('Alice', 'Bob')
    g.add_edge('Bob', 'Carol')
    g.add_edge('Bob', 'Dave')
    g.add_edge('Bob', 'Ed')
    g.add_edge('Dave', 'Ed')
    g.add_edge('Dave', 'Fred')
    g.add_edge('Dave', 'Greg')
    g.add_edge('Ed', 'Greg')
    g.add_edge('Ed', 'Harry')
    g.add_edge('Fred', 'Greg')
    g.add_edge('Greg', 'Harry')
    return g


def draw_graph(g, pert, layout):
    p = int(pert*100)
    nx.draw_networkx(g, pos=layout, node_size=5, font_size=2, font_color='b', arrowsize=3)
    plt.draw()
    plt.savefig('img/pert_{}.png'.format(p), dpi=500)
    plt.close()

def get_measurements(g):
    data = pd.Series()

    data['nodes'] = len(g)
    data['edges'] = len(g.edges())
    data['components'] = nx.number_connected_components(g)

    data['diameter'] = nx.diameter(giant_comp(g))

    all_paths = dict(nx.shortest_path_length(g))
    path_lengths = [path for paths in all_paths.values() for path in paths.values()]
    data['path length'] = median(path_lengths)

    data['closeness'] = median(nx.closeness_centrality(g).values())
    data['betweenness'] = median(nx.betweenness_centrality(g).values())
    data['clustering'] = median(nx.clustering(g).values())

    return data


def hi(g, i: int):
    neighbors = {n: knbrs(g, n, i-1) for n in g.nodes()}

    res = {}
    for k,v in neighbors.items():
        if i == 0:
            res[k] = [0]
        else:
            res[k] = sorted([g.degree(n) for n in v])
    
    return res


def knbrs(g, start, k):
    nbrs = set([start])
    for l in range(k):
        nbrs = set((nbr for n in nbrs for nbr in g[n]))
    return nbrs


def eq_class(hi_dict: dict):
    eq_class = {}
    for key, degrees in hi_dict.items():
        k = tuple(sorted(degrees))
        
        if k not in eq_class:
            eq_class[k] = [] # Initialize the value field for that empty key
        
        eq_class[k].append(key)

    return eq_class


def deanonymize(g, i):
    h = hi(g, i)

    eq = eq_class(h).values()

    f = lambda vals, minv, maxv: {v[0] for v in vals if len(v) >= minv and len(v) <= maxv}

    deanonymized_nodes = {}
    
    deanonymized_nodes['1'] = f(eq, 1, 1)
    deanonymized_nodes['2-4'] = f(eq, 2, 4)
    deanonymized_nodes['5-10'] = f(eq, 5, 10)
    deanonymized_nodes['11-20'] = f(eq, 11, 20)
    deanonymized_nodes['20-inf'] = f(eq, 2, inf)

    data = pd.Series()

    #data['h{} equivalence classes'.format(i)] = len(eq)
    for k,v in deanonymized_nodes.items():
        data['h{} deanonymization [{}]'.format(i, k)] = len(v) / len(g)
    
    return data


def perturbation(graph, p):
    g = graph.copy()
    edges_to_remove = int(len(g.edges()) * p)
    
    removed_edges = []
    for i in range(edges_to_remove):
        random_edge = random.choice(list(g.edges()))
        g.remove_edges_from([random_edge])
        removed_edges.append(random_edge)

    while(edges_to_remove > 0):
        first_node = random.choice(list(g.nodes()))
        second_node = random.choice(list(g.nodes()))
        if(second_node == first_node):
            continue
        if g.has_edge(first_node, second_node) or (first_node, second_node) in removed_edges or (second_node, first_node) in removed_edges:
            continue
        else:
            g.add_edge(first_node, second_node)
            edges_to_remove -= 1
    
    return g


if __name__ == '__main__':
    #g = create_random_graph(1000, 0.005)
    #g = create_scale_free_graph(1000)
    g = create_ex_graph()
    
    layout = nx.spring_layout(g)

    measures = {}
    for pert in [0, 0.05, 0.1, 0.5, 1]:
        pert_graph = perturbation(g, pert)
        #draw_graph(pert_graph, pert, layout)

        measures[pert] = pd.concat([
            get_measurements(pert_graph),
            *[deanonymize(pert_graph, i) for i in range(0, 5)]
        ])

    df = pd.DataFrame(measures)
    print(df)
