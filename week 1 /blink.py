import serial
import time
import random
from datetime import datetime

try:
    ser = serial.Serial('COM3', 9600)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

time.sleep(2)  # Allow time for the serial connection to establish

while True:
    # Generate a random number and send it to Arduino
    send_number = random.randint(1, 10)
    print(f"{datetime.now()} - Sending: {send_number}")
    ser.write(f"{send_number}\n".encode())

    # Read the response from Arduino
    response = ser.readline().decode().strip()
    print(f"{datetime.now()} - Received: {response}")

    # Extract the number from the response string
    if "Response number:" in response:
        response_number = int(response.split(":")[1].strip())
        print(f"{datetime.now()} - Sleeping for: {response_number} seconds")
        time.sleep(response_number)
    else:
        print(f"{datetime.now()} - Non-integer data received: {response}")
