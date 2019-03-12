from random import choice
import networkx as nx


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
    for i in range(k):
        nbrs = set((nbr for n in nbrs for nbr in g[n]))
    return nbrs


def edge_facts_subgraph(graph, n):
    g = get_subgraph(graph, n)

    pass
    return hi(g, 1)


def get_subgraph(g, n):
    start = choice(list(g))

    graph = nx.Graph()
    graph.add_node(start)

    for node, edges in nx.bfs_successors(g, start):
        for edge in edges:
            if n == 0:
                break
            
            graph.add_edge(node, edge)
            n -= 1

    return graph

