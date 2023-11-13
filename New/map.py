import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

locations = ["A", "B", "C", "D", "E", "F", "G", "H"]
G.add_nodes_from(locations)

edges = [("A", "B"),("B", "G"),("G", "H"),("A", "D"),("D", "H"),("A", "C"),("C", "E"),("E", "F"),("F", "H"), ("E", "D")]
G.add_edges_from(edges)

pos = nx.spring_layout(G) 
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)

plt.savefig("test_map_2.png")
plt.show()
