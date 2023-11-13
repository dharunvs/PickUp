import random
import json as JSON

def generateData(filename, count, passenger=False):
    locations = ["A", "B", "C", "D", "E", "F", "G", "H"]
    time = ["07:00:00", "08:00:00", "09:00:00", "19:00:00", "20:00:00"]
    day = ["2023-10-01", "2023-11-02", "2023-11-03", "2023-11-04"]
    json = []
    route = {"routes": {"legs": {"steps": []}}}
    for i in range(count):
        route = {"routes": {"legs": {"steps": []}}}
        length = random.randint(2, len(locations) - 2)
        
        if passenger:
            steps = random.sample(locations, 2)
            pickupTime = f'{random.choice(["07","08","13","14","19","20"])}:{int(random.randint(0,59))}:00'
            pickupTime = f'{random.randint(0,23)}:{int(random.randint(0,59))}:00'
            pickupDay = random.choice(day)
            time = f"{pickupDay} {pickupTime}"
            route["time"] = time
        else:
            steps = random.sample(locations, length)
        route["routes"] = steps
        
        json.append(route)
    with open(filename, 'w') as file:
        JSON.dump(json, file)
    print(json)

def getRoutes(steps):
    rider_routes = loadJSON("riderRoutes.json")
    possible_routes = []
    for route in rider_routes:
        rider_steps = route["routes"]
        if checkRoute(steps, rider_steps):
            possible_routes.append(route)
    possible_routes = sorted(
        possible_routes, key=lambda x: len(x["routes"]))
    return possible_routes

def checkRoute(steps, rider_steps):
    m, n = len(steps), len(rider_steps)
    for i in range(n - m + 1):
        if rider_steps[i:i + m] == steps:
            return True
    return False

def loadJSON(filename):
    with open(filename, 'r') as file:
        array = JSON.load(file)
    return (array)

def passengerFrequency():
    passenger_routes = loadJSON("passengerRoutes.json")
    passenger_routes = [f'{x["routes"][0]},{x["routes"][1]}' for x in passenger_routes]
    passenger_routes_distinct = list(set(passenger_routes))
    s = ""
    for i in passenger_routes_distinct:
        s += f"{i.split(',')[0]}-{i.split(',')[1]},{passenger_routes.count(i)}\n"
    print(s)
    passenger_frequency = sorted([[i.split(","), passenger_routes.count(i)] for i in passenger_routes_distinct], key = lambda x : -x[1])
    s = ""
    for i in passenger_frequency:
        s += f"{i[0][0]}-{i[0][1]},{i[1]}\n"
    with open("passenger_frequency.csv", "w") as file:
        file.write(s)
    return passenger_frequency

 
def passengerFrequencyByClustering():
    from sklearn.cluster import KMeans
    from collections import Counter
    data = loadJSON("passengerRoutes.json")
    steps_data = [entry["routes"] for entry in data]
    demand = []
    steps_numerical = []
    for steps in steps_data:
        numerical_steps = [ord(step) - ord('A') for step in steps]
        steps_numerical.append(numerical_steps)
    kmeans = KMeans(n_clusters=5) 
    kmeans.fit(steps_numerical)
    cluster_labels = kmeans.labels_
    step_combination_counts = {}
    for cluster_id, steps in zip(cluster_labels, steps_data):
        combination = tuple(steps)
        if combination not in step_combination_counts:
            step_combination_counts[combination] = 1
        else:
            step_combination_counts[combination] += 1
    for combination, count in step_combination_counts.items():
        demand.append([combination, count])
    demand = sorted(demand, key= lambda x: -x[1])
    print("\n")
    for i in demand:
        print(i)
    print("\n")
    return demand

def suggestRoute():
    rider_routes = loadJSON("riderRoutes.json")
    passenger_routes = loadJSON("passengerRoutes.json")

    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp

    # Extract the steps (locations) from rider routes
    rider_steps = []
    for route in rider_routes:
        steps = route["routes"]
        rider_steps.append(steps)

    # Define the number of passengers and the maximum number of stops
    num_passengers = len(passenger_routes)
    max_stops = 5  # Adjust this based on your needs

    # Create the data for the TSP with Time Windows (TSPTW)
    data = {}
    data['locations'] = rider_steps
    data['num_vehicles'] = 1
    data['depot'] = 0  # The depot is the starting and ending location (rider's home)

    # Calculate the time windows for passengers based on their pickup and drop-off locations
    time_windows = [(0, 0)]  # Rider starts from home, so no time window

    # Generate time windows for passengers
    for _ in range(num_passengers):
        time_windows.append((0, max_stops))  # Adjust time windows as needed

    data['time_windows'] = time_windows

    # Create a function to calculate time between locations (you can customize this function)
    def time_callback(from_node, to_node):
        return 1  # In this example, we assume that travel time between locations is uniform

    data['time_callback'] = time_callback

    # Instantiate the routing solver
    manager = pywrapcp.RoutingIndexManager(len(data['locations']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_callback'](from_node, to_node)

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc (here, distance is set to 1)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Define the maximum number of stops
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.time_limit.seconds = 1
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Get the route
    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        
        suggested_route = [data['locations'][node] for node in route]
        

        
        for i in range(len(suggested_route)):
            try:
                suggested_route[i].remove(rider_routes[i]["routes"][0])
            except:
                pass
            try:
                suggested_route[i].remove(rider_routes[i]["routes"][-1])
            except:
                pass
        
        rider_routes = loadJSON("riderRoutes.json")
        for i in range(len(suggested_route)):
            # suggested_route[i] = list(set(suggested_route[i]))
            suggested_route[i].insert(0, rider_routes[i]["routes"][0])
            suggested_route[i].append(rider_routes[i]["routes"][-1])
            
        rider_routes = loadJSON("riderRoutes.json")
        return rider_routes, suggested_route

# demand = passengerFrequencyByClustering()
# suggested_routes = suggestRoute()

# print("\n")
# print(f'Least Demand: {demand[-1][0][0]}->{demand[-1][0][1]}')
# print(f'Highest Demand: {demand[0][0][0]}->{demand[0][0][1]}')
# print('Current route:', suggested_routes[0][1]["routes"])
# print('Suggested route:', suggested_routes[1][1])
# print("\n")

generateData("passengerRoutes.json", 6000, True)