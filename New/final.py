from collections import Counter
import json as JSON
import numpy as np

def get_all_possible_routes():
    with open("all_possible_routes.json", "r") as file:
        json = JSON.loads(file.read())
    routes = []
    for i in json.keys():
        routes.extend(json[i])
        
    return routes

def get_passenger_routes():
    routes = []
    with open("passengerRoutes.json", "r") as file:
        json = JSON.loads(file.read())
    for i in json:
        routes.append(f'{i["routes"][0]}-{i["routes"][1]}')
    routes = list(set(routes))
    
    return routes

def get_demand():
    raw_data = JSON.load(open("passengerRoutes.json"))
    data = {
        'pick_drop': [],
    }

    for record in raw_data:
        data['pick_drop'].append(f'{record["routes"][0]}-{record["routes"][1]}')
    pickup_demand = Counter(data['pick_drop'])

    return dict(pickup_demand)


# print(get_all_possible_routes())
# print(get_passenger_routes())
# print(get_demand())


# Define the set of locations
locations = ["A", "B", "C", "D", "E", "F", "G", "H"]
passenger_routes = ["A-B", "B-C", "H-G"]
passenger_routes = get_passenger_routes()

# Define all possible routes
rider_routes = get_all_possible_routes()

# Define the demand for each location
demand = get_demand()
# Convert routes to state indices for Q-table

# Initialize Q-values
Q_values = np.zeros((len(locations), len(locations)))

# Hyperparameters
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
epsilon = 0.1  # exploration-exploitation trade-off

# Convert passenger routes to a dictionary for easy lookup
passenger_routes_dict = {route: True for route in passenger_routes}

# Convert rider routes to indices for easy manipulation
rider_routes_indices = [[locations.index(loc) for loc in route] for route in rider_routes]

# Q-learning algorithm
for episode in range(1000):
    # Randomly select a rider route
    current_route_index = np.random.randint(len(rider_routes_indices))
    current_route = rider_routes_indices[current_route_index]

    # Update Q-values based on the rider's route
    for i in range(len(current_route) - 1):
        state = current_route[i]
        next_state = current_route[i + 1]
        reward = demand.get(locations[state] + '-' + locations[next_state], 0)
        Q_values[state, next_state] = (1 - alpha) * Q_values[state, next_state] + \
                                      alpha * (reward + gamma * np.max(Q_values[next_state]))

# Choose the best action for the given rider route
def suggest_route(rider_route):
    suggested_route = [locations.index(loc) for loc in rider_route]

    for i in range(len(suggested_route) - 1):
        state = suggested_route[i]
        next_state = suggested_route[i + 1]
        if locations[state] + '-' + locations[next_state] in passenger_routes_dict:
            # Update the route to pick up passengers with high demand
            suggested_route.insert(i + 1, np.argmax(Q_values[state]))

    suggested_route = [locations[loc] for loc in suggested_route]
    return suggested_route

# Example usage
given_rider_route = ["B", "D", "H", "G", "A"]
suggested_rider_route = suggest_route(given_rider_route)

print("Given rider route:", given_rider_route)
print("Suggested rider route:", suggested_rider_route)