import random
import json as JSON


def generateData(filename):
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

    for i in range(100):
        route = {"routes": {
            "legs": {
                "steps": []
            }
        }}
        length = random.randint(2, len(locations) - 2)  # 3
        steps = random.sample(locations, length)  # ['B', 'G', 'A']
        route["routes"]["legs"]["steps"] = steps
        json.append(route)
    with open(filename, 'w') as file:
        JSON.dump(json, file)
    print(json)


def getRoutes(steps):
    rider_routes = loadJSON("data.json")
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


a = getRoutes(["E", "F"])
for i in a:
    print(i)
