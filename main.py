import networkx as nx
import pandas as pd

import anonymity
import graph
import queries

from sys import stderr


def main():
    print('creating graph...', file=stderr)

    g = graph.create_random_graph(100, 0.05)
    #g = graph.create_scale_free_graph(1000)
    #g = graph.create_ex_graph()
    #g = nx.read_edgelist('data/enron-graph.txt')
    #g = nx.read_edgelist('data/hepth-graph.txt')
    
    #layout = nx.spring_layout(g)

    measures = {}
    for pert in [0, .05, .1, .2, .5, 1]:
        print('perturbation ({:.0%} of edges)...'.format(pert), file=stderr)

        pert_graph = anonymity.perturbation(g, pert)
        #graph.draw_graph(pert_graph, pert, layout)

        print('\tmeasurements...', file=stderr)
        measurements = graph.get_measurements(pert_graph)

        print('\th...', file=stderr)
        h = [] #[anonymity.deanonymize_h(pert_graph, i) for i in range(0, 5)]
        
        print('\tedge facts...', file=stderr)
        ef = [anonymity.deanonymize_edgefacts(g, pert_graph, n) for n in range(0, 51, 5)]

        measures[pert] = pd.concat([measurements, *h, *ef])

    df = pd.DataFrame(measures)
    print(df.to_string())

    #subgraph = queries.edge_facts_subgraph(g, 5)   
    #print('Edges discovered: {} out of {}'.format(len(subgraph.edges()), len(g.edges())))

if __name__ == '__main__':
    main()