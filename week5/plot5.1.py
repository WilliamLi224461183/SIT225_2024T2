import pandas as pd
import matplotlib.pyplot as plt

# Path to your CSV file
csv_file_path = "C:/Users/ausle/Documents/Data/sensor_data.csv"

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Clean the data: remove any rows with missing or non-numeric values
df = df.dropna()  # Drop rows with any missing values
df['accelerationX'] = pd.to_numeric(df['accelerationX'], errors='coerce')
df['accelerationY'] = pd.to_numeric(df['accelerationY'], errors='coerce')
df['accelerationZ'] = pd.to_numeric(df['accelerationZ'], errors='coerce')
df = df.dropna()  # Drop rows with any non-numeric values after conversion

# Convert 'timestamp' to datetime for proper plotting
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S')

# Plot X, Y, and Z acceleration data separately
plt.figure(figsize=(10, 6))

# Plot accelerationX
plt.subplot(3, 1, 1)
plt.plot(df['timestamp'], df['accelerationX'], label='X-axis')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration X')
plt.title('Acceleration X Over Time')
plt.grid(True)

# Plot accelerationY
plt.subplot(3, 1, 2)
plt.plot(df['timestamp'], df['accelerationY'], label='Y-axis', color='green')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration Y')
plt.title('Acceleration Y Over Time')
plt.grid(True)

# Plot accelerationZ
plt.subplot(3, 1, 3)
plt.plot(df['timestamp'], df['accelerationZ'], label='Z-axis', color='red')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration Z')
plt.title('Acceleration Z Over Time')
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Save the plot as an image file
plt.savefig("C:/Users/ausle/Documents/Data/acceleration_plots.png")

# Show the plot
plt.show()

# Combined plot
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['accelerationX'], label='X-axis')
plt.plot(df['timestamp'], df['accelerationY'], label='Y-axis', color='green')
plt.plot(df['timestamp'], df['accelerationZ'], label='Z-axis', color='red')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration')
plt.title('Acceleration X, Y, Z Over Time')
plt.legend()
plt.grid(True)

# Save the combined plot as an image file
plt.savefig("C:/Users/ausle/Documents/Data/combined_acceleration_plot.png")

# Show the plot
plt.show()
