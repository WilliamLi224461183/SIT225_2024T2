import serial
import csv
import time

ser = serial.Serial('COM3', 9600)

with open('accelerometer_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'X', 'Y', 'Z'])  

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if "X:" in line:
               
                data = line.split(',')
                x = data[0].split(' ')[1]
                y = data[1].split(' ')[2]
                z = data[2].split(' ')[2]

                
                timestamp = time.strftime('%Y%m%d%H%M%S')

                
                writer.writerow([timestamp, x, y, z])
                print(f"Logged data at {timestamp}: X={x}, Y={y}, Z={z}")

        time.sleep(1)  
