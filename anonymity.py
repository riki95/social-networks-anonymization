import networkx as nx
from random import choice
from math import inf
import pandas as pd

import queries


def perturbation(graph, p):
    g = graph.copy()
    edges_to_remove = int(len(g.edges()) * p)
    
    removed_edges = []
    for i in range(edges_to_remove):
        random_edge = choice(list(g.edges()))
        g.remove_edges_from([random_edge])
        removed_edges.append(random_edge)

    while(edges_to_remove > 0):
        first_node = choice(list(g.nodes()))
        second_node = choice(list(g.nodes()))
        if(second_node == first_node):
            continue
        if g.has_edge(first_node, second_node) or (first_node, second_node) in removed_edges or (second_node, first_node) in removed_edges:
            continue
        else:
            g.add_edge(first_node, second_node)
            edges_to_remove -= 1
    
    return g


def deanonymize_h(g, i):
    h = queries.hi(g, i)

    return deanonymize(h, 'h({})'.format(i))


def deanonymize_edgefacts(g, n):
    edgefacts = queries.edge_facts_subgraph(g, n)

    return deanonymize(edgefacts, 'edgefacts({})'.format(n))


def deanonymize(facts, query_name):
    eq = eq_class(facts).values()

    f = lambda vals, minv, maxv: [len(v) for v in vals if len(v) >= minv and len(v) <= maxv]

    deanonymized_nodes = {}
    
    deanonymized_nodes['1'] = f(eq, 1, 1)
    deanonymized_nodes['2-4'] = f(eq, 2, 4)
    deanonymized_nodes['5-10'] = f(eq, 5, 10)
    deanonymized_nodes['11-20'] = f(eq, 11, 20)
    deanonymized_nodes['20-inf'] = f(eq, 20, inf)

    tot = sum([vv for v in deanonymized_nodes.values() for vv in v])

    data = pd.Series()
    for k,v in deanonymized_nodes.items():
        data['{} deanonymization [{}]'.format(query_name, k)] = sum(v) / tot
    
    return data


def eq_class(facts: dict):
    eq_class = {}
    for key, degrees in facts.items():
        k = tuple(sorted(degrees))
        
        if k not in eq_class:
            eq_class[k] = [] # Initialize the value field for that empty key
        
        eq_class[k].append(key)

    return eq_class

