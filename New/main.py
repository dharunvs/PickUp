import random
import json as JSON

def generateData(filename, count):
    '''
    [
        {
            "routes": {
            "legs": {
                "start_address": "5689 Del Sol Road",
                "end_address": "069 Bunting Plaza",
                "steps": [
                    {"start_location": { "lat": 37.0862154, "lng": 127.0391832 },
                    "end_location": { "lat": 43.368364, "lng": -1.7705346 },
                    "distance": { "value": 879 },
                    "duration": { "value": 9304 }
                    }]
                }
            }
        }
    ]'''
    locations = ["A", "B", "C", "D", "E", "F", "G", "H"]
    json = []
    route = {"routes": {
        "legs": {
            "steps": []
        }
    }}

    for i in range(count):
        route = {"routes": {
            "legs": {
                "steps": []
            }
        }}
        length = random.randint(2, len(locations) - 2)  # 3
        # steps = random.sample(locations, length)  # ['B', 'G', 'A']
        steps = random.sample(locations, 2)  # ['B', 'G', 'A']
        route["routes"]["legs"]["steps"] = steps
        json.append(route)
    with open(filename, 'w') as file:
        JSON.dump(json, file)
    print(json)

def getRoutes(steps):
    rider_routes = loadJSON("riderRoutes.json")
    possible_routes = []
    for route in rider_routes:
        rider_steps = route["routes"]["legs"]["steps"]
        if checkRoute(steps, rider_steps):
            possible_routes.append(route)

    possible_routes = sorted(
        possible_routes, key=lambda x: len(x["routes"]["legs"]["steps"]))
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
    passenger_routes = [f'{x["routes"]["legs"]["steps"][0]},{x["routes"]["legs"]["steps"][1]}' for x in passenger_routes]
    passenger_routes_distinct = list(set(passenger_routes))
    # s = ""
    # for i in passenger_routes_distinct:
    #     s += f"{i.split(',')[0]}-{i.split(',')[1]},{passenger_routes.count(i)}\n"
    # print(s)

    passenger_frequency = sorted([[i.split(","), passenger_routes.count(i)] for i in passenger_routes_distinct], key = lambda x : -x[1])
    # s = ""
    # for i in passenger_frequency:
    #     s += f"{i[0][0]}-{i[0][1]},{i[1]}\n"
    # with open("passenger_frequency.csv", "w") as file:
    #     file.write(s)
        
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import OneHotEncoder
    import pandas as pd
    
        # Sample data with a categorical variable 'Route_Type' for passengers and riders
    passenger_data = pd.DataFrame({'Route_Type': ['D', 'F', 'D', 'E', 'F']})
    rider_data = pd.DataFrame({'Route_Type': ['A', 'B', 'C', 'A', 'C']})

    # Use one-hot encoding to transform the categorical variable into numeric columns
    encoder = OneHotEncoder(sparse=False)

    # Fit and transform the passenger and rider data
    passenger_encoded = encoder.fit_transform(passenger_data[['Route_Type']])
    rider_encoded = encoder.fit_transform(rider_data[['Route_Type']])

    # Define the number of clusters (you can adjust this as needed)
    num_clusters = 30

    # Apply K-Means clustering to passenger and rider data
    passenger_kmeans = KMeans(n_clusters=num_clusters)
    rider_kmeans = KMeans(n_clusters=num_clusters)

    passenger_clusters = passenger_kmeans.fit_predict(passenger_encoded)
    rider_clusters = rider_kmeans.fit_predict(rider_encoded)
    
    print("-->", passenger_clusters)
    print("-->", rider_clusters)

    # Analyze the clusters and suggest alternate routes for riders as needed
    # Your specific analysis would depend on the characteristics of your data and business logic

    # Print the cluster assignments for passengers and riders
    print("Passenger Clusters:", passenger_clusters)
    print("Rider Clusters:", rider_clusters)
    
    data = pd.DataFrame({'Route_Type': ['D', 'F', 'D', 'E', 'F']})

    # Use one-hot encoding to transform the categorical variable into numeric columns
    encoder = OneHotEncoder(sparse=False)
    encoded_data = encoder.fit_transform(data[['Route_Type']])
    
    print(data)
    print(encoded_data)
    
    encoder = OneHotEncoder(sparse=False)
    encoded_data = encoder.fit_transform(passenger_routes)
    
    kmeans = KMeans(n_clusters=len(passenger_routes_distinct))  # Choose an appropriate number of clusters
    passenger_clusters = kmeans.fit_predict(encoded_data)
    
    print(passenger_clusters)
   
    # for i in passenger_routes_distinct:
    #     passenger_frequency.append([i.split(","), passenger_routes.count(i)])

    return passenger_frequency
 
def passengerFrequencyByClustering():
    from sklearn.cluster import KMeans
    from collections import Counter
    
    data = loadJSON("passengerRoutes.json")
    steps_data = [entry["routes"]["legs"]["steps"] for entry in data]
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
    
    for i in demand:
        print(i)

passengerFrequencyByClustering()