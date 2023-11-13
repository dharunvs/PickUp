# from datetime import datetime, timedelta
# from collections import Counter
# import json as JSON

# raw_data = JSON.load(open("passengerRoutes.json"))
# print(type(raw_data))

# data = {
#     'pickup_location': [],
#     'drop_location': [],
#     'pickup_time': [],
#     'pick_drop': [],
# }

# for record in raw_data:
#     time = record["time"]
#     data['pickup_location'].append(record["routes"][0])
#     data["drop_location"].append(record["routes"][1])
#     data["pickup_time"].append(time)
#     data['pick_drop'].append(f'{record["routes"][0]}-{record["routes"][1]}')
    
# grouped_data = {}

# dates = []
# for i in data['pickup_time']:
#     dates.append(i.split(" ")[0])

# dates = sorted(list(set(dates)), key= lambda x : int(x.split("-")[2]))

# print(dates)

# for i in dates:
#     grouped_data[i] = {
#     'pickup_location': [],
#     'drop_location': [],
#     'pickup_time': [],
#     'pick_drop': [],
# }

# for record in raw_data:
#     time = record["time"]
#     date = time.split(" ")[0]
#     grouped_data[date]['pickup_location'].append(record["routes"][0])
#     grouped_data[date]["drop_location"].append(record["routes"][1])
#     grouped_data[date]["pickup_time"].append(time)
#     grouped_data[date]['pick_drop'].append(f'{record["routes"][0]}-{record["routes"][1]}')
    
# data['pickup_time'] = [datetime.strptime(time, '%Y-%m-%d %H:%M:%S') for time in data['pickup_time']]
# data['pickup_day'] = [time + timedelta(days=1) for time in data['pickup_time']]

# next_day_data = {
#     'pickup_location': [],
#     'drop_location': [],
#     'pickup_time': [],
#     'pick_drop':[]
# }

# for i in range(len(data['pickup_time'])):
#     next_day_data['pickup_location'].append(data['pickup_location'][i])
#     next_day_data['drop_location'].append(data['drop_location'][i])
#     next_day_data['pickup_time'].append(data['pickup_time'][i])
#     next_day_data['pick_odrp'].append(data['pick_drop'][i])

# pickup_demand = Counter(next_day_data['pick_drop'])

# for i in pickup_demand.keys():
#     print(i, pickup_demand[i])

# print(dict(pickup_demand))

from collections import Counter
import json as JSON

raw_data = JSON.load(open("passengerRoutes.json"))

data = {
    'pick_drop': [],
}

for record in raw_data:
    data['pick_drop'].append(f'{record["routes"][0]}-{record["routes"][1]}')
pickup_demand = Counter(data['pick_drop'])

print(dict(pickup_demand))

