import networkx as nx
import pandas as pd

import anonymity
import graph
import queries


def main():
    #g = graph.create_random_graph(1000, 0.005)
    #g = graph.create_scale_free_graph(1000)
    #g = graph.create_ex_graph()
    #g = nx.read_edgelist('data/enron-graph.txt')
    g = nx.read_edgelist('data/hepth-graph.txt')
    
    layout = nx.spring_layout(g)

    measures = {}
    for pert in [0]:
        pert_graph = anonymity.perturbation(g, pert)
        #graph.draw_graph(pert_graph, pert, layout)
        print('pert')
        measures[pert] = pd.concat([
            graph.get_measurements(pert_graph),
            *[anonymity.deanonymize_h(pert_graph, i) for i in range(0, 5)],
            *[anonymity.deanonymize_edgefacts(pert_graph, n) for n in range(0, 10, 5)]
        ])

    df = pd.DataFrame(measures)
    print(df)

    #subgraph = queries.edge_facts_subgraph(g, 5)   
    #print('Edges discovered: {} out of {}'.format(len(subgraph.edges()), len(g.edges())))

if __name__ == '__main__':
    main()