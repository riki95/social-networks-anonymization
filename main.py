import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
    g = nx.fast_gnp_random_graph(50,0.09)
    #g = g.to_undirected()
    return g

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


def draw_graph(g):
    nx.draw(g, pos=nx.spring_layout(g), node_size=50, font_size=6, font_color='w', arrowsize=3)
    plt.draw()
    plt.savefig('img.png', dpi=500)
    plt.close()


def compute_degree(g):
    degree = g.degree()

    total_degree = 0
    max_degree = 0
    min_degree = g.number_of_nodes()
    for node, degree_node in degree:
        total_degree = total_degree + degree_node
        if (degree_node > max_degree):
            max_degree = degree_node
        if (degree_node < min_degree):
            min_degree = degree_node
        #print(node, degree_node)

    return total_degree, max_degree, min_degree


def print_measurements(g):
    number_of_nodes = g.number_of_nodes()
    print('Number of nodes:', number_of_nodes)
    print('Number of edges:', g.number_of_edges())
    print('Number of self-loops:', g.number_of_selfloops())
    
    total_degree, max_degree, min_degree = compute_degree(g)
    print('\nTotal Degree: ', total_degree/number_of_nodes)
    print('Max Degree: ', max_degree)
    print('Min Degree: ', min_degree)


def h1(g):
    degree = g.degree()
    print('H1: ', degree)

    values = set(map(lambda x:x[1], degree))
    equivalence_class = [[y[0] for y in degree if y[1]==x] for x in values]
    print('H1 Eq_Class: ', equivalence_class)


def h2(g):
    my_dict = {}
    for n in g:
        list_values = []
        for s, e in g.edges(n):
            list_values.append(g.degree(e))
        #print(list_values)
        my_dict[n] = list_values
    print('H2: ', my_dict)


if __name__ == '__main__':
    #g = create_graph()
    g = create_ex_graph()
    print_measurements(g)
    h1(g)
    h2(g)
    #draw_graph(g)