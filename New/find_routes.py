import heapq

def dijkstra(graph, start, end):
    heap = [(0, start, [])]
    visited = set()

    while heap:
        (cost, current, path) = heapq.heappop(heap)

        if current not in visited:
            visited.add(current)
            path = path + [current]

            if current == end:
                return path, cost

            for neighbor, c in graph[current].items():
                heapq.heappush(heap, (cost + c, neighbor, path))

    return None, float('inf')

def find_alternate_routes(graph, start, end, route):
    original_path, original_cost = dijkstra(graph, start, end)

    alternate_routes = []
    stack = [(start, [start])]
    
    while stack:
        (current, path) = stack.pop()
        for neighbor in graph[current]:
            if neighbor not in path:
                new_path = path + [neighbor]
                new_cost = sum(graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
                if new_cost <= original_cost:
                    stack.append((neighbor, new_path))
                    if neighbor == end and new_cost == original_cost:
                        alternate_routes.append(new_path)

    return alternate_routes

# Define the graph
nodes = ["A", "B", "C", "D", "E", "F", "G", "H"]
edges = [("A", "B"), ("B", "G"), ("G", "H"), ("A", "D"), ("D", "H"), ("A", "C"), ("C", "E"), ("E", "F"), ("F", "H"), ("E", "D")]

graph = {node: {} for node in nodes}

for edge in edges:
    graph[edge[0]][edge[1]] = 1
    graph[edge[1]][edge[0]] = 1

# Define the route
route = ["A", "B", "G", "H"]

# Find alternate routes
alternate_routes = find_alternate_routes(graph, "A", "H", route)

# Print results
print("Original route:", route)
print("Alternate routes:")
for alternate_route in alternate_routes:
    print(alternate_route)
