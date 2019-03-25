import networkx as nx

multi = nx.MultiGraph()
g = nx.read_edgelist('enron.txt', create_using=multi)

print(nx.info(g))

g2 = nx.Graph()

for u,v in g.edges():
    noe = g.number_of_edges(u,v)                # Cardinality of the edge
    if noe > 5:
        g2.add_edge(u,v)                        # Add Edge if cardinality is 5 or more

print(nx.info(g2))