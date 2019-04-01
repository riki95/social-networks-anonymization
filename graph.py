import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from statistics import median
from sys import stderr


def giant_comp(g):
    return max(nx.connected_component_subgraphs(g), key=len)


def read_graph(path, name):
    g = nx.read_edgelist(path)
    g.name = name

    return g


def create_random_graph(n, p):
    g = nx.fast_gnp_random_graph(n, p)
    g.name = 'random-{}'.format(n)

    return giant_comp(g)


def create_scale_free_graph(n):
    g = nx.scale_free_graph(n)
    g.name = 'scale-free-{}'.format(n)

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

    g.name = 'example'

    return g


def draw_graph(g, pert, layout):
    p = int(pert*100)
    nx.draw_networkx(g, pos=layout, node_size=5, font_size=2, font_color='b', arrowsize=3)
    plt.draw()
    plt.savefig('img/pert_{}.png'.format(p), dpi=500)
    plt.close()


def get_measurements(g):
    data = pd.Series()

    print('      nodes...\t\r', file=stderr, end='\n')
    data['nodes'] = len(g)

    print('      edges...\t\r', file=stderr, end='\n')
    data['edges'] = len(g.edges())

    print('      components...\t\r', file=stderr, end='\n')
    data['components'] = nx.number_connected_components(g)

    print('      diameter...\t\r', file=stderr, end='\n')
    data['diameter'] = nx.diameter(giant_comp(g))

    '''
    print('      path length...\t\r', file=stderr, end='\n')
    all_paths = dict(nx.shortest_path_length(g))
    path_lengths = [path for paths in all_paths.values() for path in paths.values()]
    data['path length'] = median(path_lengths)
    '''
    print('      closeness...\t\r', file=stderr, end='\n')
    data['closeness'] = median(nx.closeness_centrality(g).values())

    print('      betweenness...\t\r', file=stderr, end='\n')
    data['betweenness'] = median(nx.betweenness_centrality(g).values())

    print('      clustering...\t\r', file=stderr, end='\n')
    data['clustering'] = median(nx.clustering(g).values())

    return data
