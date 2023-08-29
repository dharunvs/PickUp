import json

with open("MOCK_DATA.json", "r") as f:
    data = json.load(f)


# for i in data:
#     print(i[routes])

routes = []
routes_str = []

for i in data:
    routes.append({"start": i["routes"]["legs"]["start_address"], "end": i["routes"]["legs"]["end_address"]})


for i in routes:
    routes_str.append(str(i))

routes_str = set(routes_str)

print(len(routes))
print(len(routes_str))