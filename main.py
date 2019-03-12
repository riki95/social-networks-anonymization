import networkx as nx
import pandas as pd

import anonymity
import graph


def main():
    #g = graph.create_random_graph(1000, 0.005)
    #g = graph.create_scale_free_graph(1000)
    g = graph.create_ex_graph()
    #g = nx.read_edgelist('data/enron-graph.txt')
    
    layout = nx.spring_layout(g)

    measures = {}
    for pert in [0, 0.05, 0.1, 0.5, 1]:
        pert_graph = anonymity.perturbation(g, pert)
        #graph.draw_graph(pert_graph, pert, layout)

        measures[pert] = pd.concat([
            graph.get_measurements(pert_graph),
            *[anonymity.deanonymize(pert_graph, i) for i in range(0, 5)]
        ])

    df = pd.DataFrame(measures)
    print(df)


if __name__ == '__main__':
    main()