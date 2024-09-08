import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

data = pd.read_csv(r'C:\Users\ausle\Documents\Data\week6\sensor_data.csv')
X = data[['Temperature']].values
y = data['Humidity'].values

model = LinearRegression()
model.fit(X, y)

min_temp = X.min()
max_temp = X.max()

test_temps = np.linspace(min_temp, max_temp, 100).reshape(-1, 1)
predicted_humidities = model.predict(test_temps)

plt.scatter(X, y, color='blue')
plt.plot(test_temps, predicted_humidities, color='red')
plt.xlabel('Temperature')
plt.ylabel('Humidity')
plt.show()

lower_threshold = data['Temperature'].quantile(0.05)
upper_threshold = data['Temperature'].quantile(0.95)

filtered_data = data[(data['Temperature'] > lower_threshold) & (data['Temperature'] < upper_threshold)]
X_filtered = filtered_data[['Temperature']].values
y_filtered = filtered_data['Humidity'].values

model_filtered = LinearRegression()
model_filtered.fit(X_filtered, y_filtered)

test_temps_filtered = np.linspace(X_filtered.min(), X_filtered.max(), 100).reshape(-1, 1)
predicted_humidities_filtered = model_filtered.predict(test_temps_filtered)

plt.scatter(X_filtered, y_filtered, color='blue')
plt.plot(test_temps_filtered, predicted_humidities_filtered, color='red')
plt.xlabel('Temperature')
plt.ylabel('Humidity')
plt.show()
