from itertools import combinations
import networkx as nx
import json as JSON
import matplotlib.pyplot as plt


def save_json(dict, filename):
    with open(filename, "w") as file:
        JSON.dump(dict, file)
        
def get_graph(locations, edges):
    G = nx.Graph()
    G.add_nodes_from(locations)
    G.add_edges_from(edges)

    return G

def save_graph_png(G, filename):
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)

    plt.savefig(filename)
    plt.show()

def get_all_possible_routes(G, locations):
    combinations_list = list(combinations(locations, 2))
    print(combinations_list)

    all_possible_routes = {}

    for i in combinations_list:
        start_location, end_location = i
        all_routes = list(nx.all_simple_paths(G, source=start_location, target=end_location))
        all_routes = sorted(all_routes, key= lambda x : len(x)) 
        all_possible_routes[f"{start_location}-{end_location}"] = all_routes

    return all_possible_routes
    
if __name__ == "__main__":
    
    locations = ["A", "B", "C", "D", "E", "F", "G", "H"]
    edges = [("A", "B"),("B", "G"),("G", "H"),("A", "D"),("D", "H"),("A", "C"),("C", "E"),("E", "F"),("F", "H"), ("E", "D")]
    
    G = get_graph(locations, edges)
    # save_graph_png(G, "test_1.png")

    all_possible_routes = get_all_possible_routes(G, locations)
    # save_json(all_possible_routes, "test_routes.json")
    
    s = ""
    count = 1
    for i in all_possible_routes.keys():
        s+=f"'{i}' : '{count}',\n"
        count += 1
    print(s)
    
    

