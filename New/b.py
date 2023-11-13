import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import json as JSON

# Sample data
raw_data = JSON.load(open("passengerRoutes.json"))
print(type(raw_data))

# Create a DataFrame from the given data
data = {
    'pickup_location': ['A', 'B', 'C', 'A', 'B'],
    'drop_location': ['B', 'C', 'A', 'C', 'A'],
    'pickup_time': ['2023-11-13 08:00:00', '2023-11-13 09:30:00', '2023-11-13 10:15:00', '2023-11-13 12:45:00', '2023-11-13 14:00:00'],
}

data = {
    'pickup_location': [],
    'drop_location': [],
    'pickup_time': [],
}


for record in raw_data:
    data['pickup_location'].append(record["routes"][0])
    data["drop_location"].append(record["routes"][1])
    time = record["time"]
    data["pickup_time"].append(time)

# Create a DataFrame
df = pd.DataFrame(data)

# Convert pickup_time to datetime
df['pickup_time'] = pd.to_datetime(df['pickup_time'])

# Label encode pickup and drop locations
df['pickup_location'] = df['pickup_location'].astype('category').cat.codes
df['drop_location'] = df['drop_location'].astype('category').cat.codes

# Extract features and target variable
X = df[['pickup_location', 'drop_location']]
y = df['pickup_time']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Plot the actual vs. predicted pickup times
plt.scatter(y_test, predictions)
plt.xlabel('Actual Pickup Time')
plt.ylabel('Predicted Pickup Time')
plt.title('Actual vs. Predicted Pickup Times')
plt.show()
