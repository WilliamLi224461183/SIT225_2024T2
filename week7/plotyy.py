import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go

file_path = r"C:\Users\ausle\Documents\Data\week7\sensor_data.csv"
data = pd.read_csv(file_path)

print(data.head())

X = data['Temperature'].values.reshape(-1, 1)
y = data['Humidity']

model = LinearRegression()
model.fit(X, y)

print(f"Intercept: {model.intercept_}, Slope: {model.coef_[0]}")

temp_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
predicted_humidity = model.predict(temp_range)

fig = px.scatter(data, x='Temperature', y='Humidity', title="Temperature vs Humidity")
fig.add_traces(go.Scatter(x=temp_range.flatten(), y=predicted_humidity, mode='lines', name='Regression Line'))
fig.show()

min_value = X.min() + 1
max_value = X.max() - 1

filtered_data = data[(data['Temperature'] > min_value) & (data['Temperature'] < max_value)]

X_filtered = filtered_data['Temperature'].values.reshape(-1, 1)
y_filtered = filtered_data['Humidity']
model_filtered = LinearRegression()
model_filtered.fit(X_filtered, y_filtered)

predicted_humidity_filtered = model_filtered.predict(temp_range)

fig.add_traces(go.Scatter(x=temp_range.flatten(), y=predicted_humidity_filtered, mode='lines', name='Filtered Regression Line'))
fig.show()

print(f"Filtered Intercept: {model_filtered.intercept_}, Filtered Slope: {model_filtered.coef_[0]}")
