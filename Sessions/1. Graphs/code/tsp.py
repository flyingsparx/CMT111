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
                G.add_edge(node, node2, distance=random.randint(1, 30))

    return G

def greedy_travelling_salesman(G, start_node):
    visited_cities = []
    visited_cities.append(start_node)
    
    while len(visited_cities) < G.number_of_nodes():
        smallest_distance = 50
        next_city = None
        current_city = visited_cities[-1]
    
        for edge in G.edge[current_city]:
            potential_distance = G.edge[current_city][edge]['distance']
            potential_city = edge
            if potential_distance < smallest_distance and potential_city not in visited_cities:
                smallest_distance = potential_distance
                next_city = potential_city

        visited_cities.append(next_city)
    return visited_cities
            
G = get_random_graph(10, 0.3)
visited_cities = greedy_travelling_salesman(G, G.nodes()[0])
print visited_cities
