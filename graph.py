import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from statistics import median


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