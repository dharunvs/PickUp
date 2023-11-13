from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import json as JSON
import pandas as pd

raw_data = JSON.load(open("passengerRoutes.json"))
print(type(raw_data))

data = {
    'pickup_location': [],
    'drop_location': [],
    'pickup_time': [],
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

for record in raw_data:
    data['pickup_location'].append(record["routes"][0].replace(record["routes"][0], location_int_map[record["routes"][0]]))
    data["drop_location"].append(record["routes"][1].replace(record["routes"][1], location_int_map[record["routes"][1]]))
    data["pickup_time"].append(record["time"])


df = pd.DataFrame(data)
print(df)

df['pickup_time'] = pd.to_datetime(df['pickup_time'])
df['day_of_week'] = df['pickup_time'].dt.dayofweek
df['hour_of_day'] = df['pickup_time'].dt.hour

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

features = ['pickup_location', 'drop_location', 'day_of_week', 'hour_of_day']
target = "pickup_time"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, predictions))
# print("Classification Report:\n", classification_report(y_test, predictions))

import matplotlib.pyplot as plt
import seaborn as sns

# Countplot of ride status
plt.figure(figsize=(6, 4))
sns.countplot(x='ride_status', data=df)
plt.title('Ride Status Count')
plt.show()

# Scatterplot of ride duration vs. hour of the day
plt.figure(figsize=(10, 6))
sns.scatterplot(x='hour_of_day', y='ride_duration', hue='ride_status', data=df)
plt.title('Ride Duration vs. Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Ride Duration (seconds)')
plt.show()

# Pairplot for numerical features
numerical_features = ['ride_duration', 'day_of_week', 'hour_of_day']
sns.pairplot(df[numerical_features + [target]], hue=target)
plt.suptitle('Pairplot of Numerical Features', y=1.02)
plt.show()
