import networkx as nx
import matplotlib.pyplot as plt
import random

def get_random_graph(size, density):
    G = nx.Graph()
    
    for i in range(size):
        G.add_node(i)

    for node in G.nodes():
        for node2 in G.nodes():
            if random.random() < density:
                G.add_edge(node, node2)

    return G

G = get_random_graph(10, 1)

nx.draw(G)
plt.show()
