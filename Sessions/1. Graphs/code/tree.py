import networkx as nx
import matplotlib.pyplot as plt

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return self.name+" ("+str(self.age)+")"


G = nx.DiGraph()

grandfather1 = Person("Grandfather 1", 80)
grandmother1 = Person("Grandmother 1", 76)
grandfather2 = Person("Grandfather 2", 75)
grandmother2 = Person("Grandmother 2", 77)

mother = Person("Mother", 50)
father = Person("Father", 51)
aunt = Person("Aunt", 48)

will = Person("Will", 26)
brother = Person("Brother", 24)

G.add_edge(grandfather1, grandmother1)
G.add_edge(grandmother1, mother)
G.add_edge(grandfather2, grandmother2)
G.add_edge(grandmother2, father)
G.add_edge(grandmother2, aunt)
G.add_edge(father, mother)
G.add_edge(mother, will)
G.add_edge(mother, brother)

print G.successors(mother)

nx.draw_networkx(G)
plt.show()
