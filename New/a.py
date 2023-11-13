# print('\n')
# print('Least Demand: E->A')
# print('Highest Demand: G->D')
# print('Current route: ["B", "F", "E", "A", "H"]')
# print('Suggested route: ["B", "F", "G", "D", "H"]')

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime
import json as JSON

# Sample data
raw_data = JSON.load(open("passengerRoutes.json"))
print(type(raw_data))

data = {
    'pickup_location': [],
    'drop_location': [],
    "pick_drop_int": [],
    'pickup_time': [],
    'time_int': []
}

location_int_map = {
    "A":"1",
    "B":"2",
    "C":"3",
    "D":"4",
    "E":"5",
    "F":"6",
    "G":"7",
    "H":"8",
}

route_int_map = {
    'A-B' : '1',
    'A-C' : '2',
    'A-D' : '3',
    'A-E' : '4',
    'A-F' : '5',
    'A-G' : '6',
    'A-H' : '7',
    'B-C' : '8',
    'B-D' : '9',
    'B-E' : '10',
    'B-F' : '11',
    'B-G' : '12',
    'B-H' : '13',
    'C-D' : '14',
    'C-E' : '15',
    'C-F' : '16',
    'C-G' : '17',
    'C-H' : '18',
    'D-E' : '19',
    'D-F' : '20',
    'D-G' : '21',
    'D-H' : '22',
    'E-F' : '23',
    'E-G' : '24',
    'E-H' : '25',
    'F-G' : '26',
    'F-H' : '27',
    'G-H' : '28',
}

for record in raw_data:
    data['pickup_location'].append(record["routes"][0].replace(record["routes"][0], location_int_map[record["routes"][0]]))
    data["drop_location"].append(record["routes"][1].replace(record["routes"][1], location_int_map[record["routes"][1]]))
    try:
        data["pick_drop_int"].append(route_int_map[f"{record['routes'][0]}-{record['routes'][1]}"])
    except:
        data["pick_drop_int"].append(route_int_map[f"{record['routes'][1]}-{record['routes'][0]}"])
    
    time = record["time"]
    data["pickup_time"].append(time)
    dt_object = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    timestamp = dt_object.timestamp()
    timestamp_integer = int(timestamp)
    data["time_int"].append(timestamp_integer)


df = pd.DataFrame(data)
print(df)

# Convert pickup_time to datetime object
# df['pickup_time'] = pd.to_datetime(df['pickup_time'])

# Define features (X) and target variable (y)
features = ['pick_drop_int']
target = 'time_int'

X = df[features]
y = df[target]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Train a simple linear regression model
# model = LinearRegression()
model = LogisticRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Convert predictions and actual pickup times to numeric values for visualization
# predicted_numeric = predictions.astype(int)
# actual_numeric = y_test.astype(int)

# Plotting
plt.figure(figsize=(13, 6))

# plt.scatter(X_train['pick_drop_int'], y_train, color='blue', label='Actual Pickup Time')
plt.scatter(X_test['pick_drop_int'], predictions, color='blue', label='Actual Pickup Time')

# plt.scatter(X_test['pick_drop_int'], predictions, color='blue', label='Actual Pickup Time')
# plt.scatter(X_test['pick_drop_int'], y_test, color='red', label='Predicted Pickup Time')

# plt.plot(X_test['pick_drop_int'], predictions, marker='o', linestyle='-', color='blue', label='Actual Pickup Time')
# plt.plot(X_test['pick_drop_int'], y_test, marker='o', linestyle='-', color='red', label='Predicted Pickup Time')

plt.title('Actual vs. Predicted Pickup Time')
plt.xlabel('Pick Drop Int')
plt.ylabel('Pickup Time (Numeric)')
plt.legend()
plt.show()

