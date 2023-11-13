import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Create a DataFrame from the data
data = {
    'pickup_location': ['A', 'B', 'C', 'A', 'B'],
    'drop_location': ['B', 'C', 'A', 'C', 'A'],
    'pickup_time': ['2023-11-13 08:00:00', '2023-11-13 09:30:00', '2023-11-13 10:15:00', '2023-11-14 12:45:00', '2023-11-14 14:00:00'],
}

df = pd.DataFrame(data)

# Convert pickup_time to datetime
df['pickup_time'] = pd.to_datetime(df['pickup_time'])

# Extract features from pickup_time
df['hour'] = df['pickup_time'].dt.hour
df['day_of_week'] = df['pickup_time'].dt.dayofweek

# Label encode categorical columns
le = LabelEncoder()
df['pickup_location'] = le.fit_transform(df['pickup_location'])
df['drop_location'] = le.fit_transform(df['drop_location'])

# Split the data into training and testing sets
X = df[['pickup_location', 'drop_location', 'hour', 'day_of_week']]
y = df['pickup_time']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions for 2023-11-15
new_data = {
    'pickup_location': ['A'],
    'drop_location': ['B'],
    'hour': [8],
    'day_of_week': [datetime.strptime('2023-11-15', '%Y-%m-%d').weekday()],
}

new_df = pd.DataFrame(new_data)

# Label encode categorical columns
new_df['pickup_location'] = le.transform(new_df['pickup_location'])
new_df['drop_location'] = le.transform(new_df['drop_location'])

# Make predictions
predicted_time = model.predict(new_df)
predicted_time_formatted = pd.to_datetime(predicted_time[0]).strftime('%Y-%m-15 %H:%M:%S')

print("Predicted Pickup Time:", predicted_time_formatted)


# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder
# from datetime import datetime

# # Create a DataFrame from the data
# data = {
#     'pickup_location': ['A', 'B', 'A', 'A', 'A'],
#     'drop_location': ['B', 'C', 'A', 'B', 'B'],
#     'pickup_time': ['2023-11-13 08:00:00', '2023-11-13 09:30:00', '2023-11-13 10:15:00', '2023-11-14 12:45:00', '2023-11-14 14:00:00'],
# }

# df = pd.DataFrame(data)

# # Convert pickup_time to datetime
# df['pickup_time'] = pd.to_datetime(df['pickup_time'])

# # Extract features from pickup_time
# df['hour'] = df['pickup_time'].dt.hour
# df['day_of_week'] = df['pickup_time'].dt.dayofweek

# # Label encode categorical columns
# le = LabelEncoder()
# df['pickup_location'] = le.fit_transform(df['pickup_location'])
# df['drop_location'] = le.fit_transform(df['drop_location'])

# # Define a function to classify demand as high or low
# def classify_demand(row):
#     # You can define your own criteria for high or low demand
#     return 1 if row['hour'] >= 12 else 0

# # Create the target variable 'demand'
# df['demand'] = df.apply(classify_demand, axis=1)

# # Split the data into training and testing sets
# X = df[['pickup_location', 'drop_location', 'hour', 'day_of_week']]
# y = df['demand']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train a logistic regression model
# model = LogisticRegression()
# model.fit(X_train, y_train)

# # Make predictions for a new route
# new_data = {
#     'pickup_location': ['A'],
#     'drop_location': ['B'],
#     'hour': [8],
#     'day_of_week': [datetime.strptime('2023-11-15', '%Y-%m-%d').weekday()],
# }

# new_df = pd.DataFrame(new_data)

# # Label encode categorical columns
# new_df['pickup_location'] = le.transform(new_df['pickup_location'])
# new_df['drop_location'] = le.transform(new_df['drop_location'])

# # Make predictions
# predicted_demand = model.predict(new_df)

# for i in predicted_demand:
#     print(i)

# if predicted_demand[0] == 1:
#     print("Predicted High Demand for the route.")
# else:
#     print("Predicted Low Demand for the route.")
