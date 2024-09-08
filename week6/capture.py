import serial
import pandas as pd
from datetime import datetime

ser = serial.Serial('COM3', 9600)
ser.flush()

columns = ['Timestamp', 'Humidity', 'Temperature']
data = []

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if 'Humidity' in line and 'Temperature' in line:
                parts = line.split(' ')
                humidity = float(parts[1].replace('%', ''))
                temperature = float(parts[4].replace('°C', ''))
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data.append([timestamp, humidity, temperature])
                
                df = pd.DataFrame(data, columns=columns)
                df.to_csv(r'C:\Users\ausle\Documents\Data\week6\sensor_data.csv', index=False)
                print(f"Data recorded: {timestamp}, Humidity: {humidity}%, Temperature: {temperature}°C")

except KeyboardInterrupt:
    print("Recording stopped.")
    ser.close()
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(r'C:\Users\ausle\Documents\Data\week6\sensor_data.csv', index=False)
    print("Final data saved to sensor_data.csv")
