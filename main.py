import networkx as nx
import matplotlib.pyplot as plt


def create_graph():
    g = nx.fast_gnp_random_graph(50,0.09)
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
    h1 = g.degree()
    print('\nH1: ', h1)

    values = set(map(lambda x:x[1], h1))
    eq_class_h1 = [[y[0] for y in h1 if y[1]==x] for x in values]
    print('H1 Eq_Class: ', eq_class_h1)


def h2(g):
    h2_dict = {}
    for node in g:
        list_values = []
        for start, end in g.edges(node):
            list_values.append(g.degree(end))
        h2_dict[node] = list_values
    print('\nH2: ', h2_dict)

    eq_class_h2 = {}
    for key in h2_dict:
        s = ''
        list_values = []
        for value in h2_dict[key]:
            s += str(value)  # We convert the list into a string to let it be the key
        if (eq_class_h2.get(s) == None):
            eq_class_h2[s] = list_values  # Initialize the value field for that empty key
        eq_class_h2[s].append(key)

    print ('H2 Eq_Class: ', eq_class_h2)   


def h3(g):
    h3_dict = {}
    for node in g:
        list_values = []
        for start, end in g.edges(node):
            for start2, end2 in g.edges(end):
                list_values.append(g.degree(end2))
        h3_dict[node] = list_values
    print('\nH3: ', h3_dict)

    eq_class_h3 = {}
    for key in h3_dict:
        s = ''
        list_values = []
        for value in h3_dict[key]:
            s += str(value)  # We convert the list into a string to let it be the key
        if (eq_class_h3.get(s) == None):
            eq_class_h3[s] = list_values  # Initialize the value field for that empty key
        eq_class_h3[s].append(key)

    print ('H3 Eq_Class: ', eq_class_h3)  


if __name__ == '__main__':
    #g = create_graph()
    g = create_ex_graph()

    print_measurements(g)
    h1(g)
    h2(g)
    h3(g)

    #draw_graph(g)