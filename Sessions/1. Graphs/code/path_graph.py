import networkx as nx
import matplotlib.pyplot as plt

def get_path_graph(size):
    G = nx.Graph()
    
    for i in range(size):
        G.add_node(i)

    nodes = G.nodes()
    for i,node in enumerate(nodes):
        if i < len(nodes)-1:
            G.add_edge(nodes[i], nodes[i+1])
        
    return G

G = get_path_graph(10)

nx.draw(G)
plt.show()
