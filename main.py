import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(g):
    nx.draw(g, pos=nx.spring_layout(g), node_size=50, font_size=6, font_color='w', arrowsize=3)
    plt.draw()
    plt.savefig('img.png', dpi=500)
    plt.close()

def main():
    g = nx.fast_gnp_random_graph(50,0.075)
    g = g.to_undirected()
    draw_graph(g)


if __name__ == '__main__':
    main()