import networkx as nx
import matplotlib.pyplot as plt
import random


def create_random_graph(n, p):
    g = nx.fast_gnp_random_graph(n, p)
    gc = max(nx.connected_component_subgraphs(g), key=len)
    return gc


def create_scale_free_graph(n):
    return nx.scale_free_graph(n)


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


def draw_graph(g, name):
    nx.draw_networkx(g, pos=nx.spring_layout(g), node_size=50, font_size=10, font_color='b', arrowsize=3)
    plt.draw()
    plt.savefig('{}.png'.format(name), dpi=500)
    plt.close()

def print_measurements(g):
    print(nx.info(g))

    # TODO: check if it can be refactored in a better way
    l = []
    for n, degree in g.degree():
        l.append(degree)
    l = sorted(l)
    print ('Median: ', l[int(len(l)/2)])


def hi(g, i: int):
    neighbors = {n: knbrs(g, n, i-1) for n in g.nodes()}

    res = {}
    for k,v in neighbors.items():
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
    eq = eq_class(h)

    deanonymized_nodes = {v[0] for k,v in eq.items() if len(v) == 1}

    print('[h{}] {} nodes'.format(i, len(g)))
    print('[h{}] {} equivalence classes ({:.0%})'.format(i, len(eq), len(eq) / len(g)))

    print('[h{}] {:.0%} deanonymization'.format(i, len(deanonymized_nodes) / len(g)))
    
    print()


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
    #g = create_random_graph(500, 0.01)
    #g = create_scale_free_graph(500)
    g = create_ex_graph()

    print_measurements(g)

    #for i in range(1, 5):
    #    deanonymize(g, i)
    
    #for k,v in eq.items():
    #    print('{}: {}'.format(k,v))

    #draw_graph(g, 'before_perturbation')

    pert_list = [0.05, 0.1, 0.5, 1]
    for pert in pert_list:
        print('\n\tPerturbation: ', pert)
        pert_graph = perturbation(g, pert)
        print_measurements(pert_graph)
        
    #draw_graph(pert_graph, 'after_perturbation')