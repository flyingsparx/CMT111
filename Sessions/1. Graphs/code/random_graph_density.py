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

degrees = []
densities = []

for i in range(0, 100):
    density = float(i)/100.0
    G = get_random_graph(10, density)

    total_degree = 0
    for node in G.nodes():
        total_degree += nx.degree(G, node)
    average_degree = total_degree/nx.number_of_nodes(G)
    
    degrees.append(average_degree)
    densities.append(density)

plt.plot(densities, degrees)
plt.show()
