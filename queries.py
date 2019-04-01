from random import choice
import networkx as nx

from sys import stderr


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


def edge_facts_subgraph(g, g_pert, n):
    res = {}

    nodes_no = len(g.nodes) * len(g_pert.nodes)
    i = 0

    for start in g.nodes:
        fact = get_subgraph(g, n, start)

        res[start] = []

        for node in g_pert.nodes:
            subgraphs = [get_subgraph(g_pert, n, node)] # should instead get all possible subgraphs

            for subgraph in subgraphs:
                if nx.is_isomorphic(fact, subgraph):
                    res[start].append(node)

            i += 1
            print('[{}] {:.3%}\t\r'.format(n, i/nodes_no), file=stderr, end='')

    return res


def get_subgraph(g, n, start):
    graph = nx.Graph()
    graph.add_node(start)

    for node, edges in nx.bfs_successors(g, start):
        for edge in edges:
            if n == 0:
                break

            graph.add_edge(node, edge)
            n -= 1

    return graph

