#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include <Arduino_LSM6DS3.h>
#include <Wire.h>
#include <WiFiNINA.h>

const char SSID[] = "99 Banana's";
const char PASS[] = "G0439999998";

float accelerationX;
float accelerationY;
float accelerationZ;

WiFiConnectionHandler connectionHandler(SSID, PASS);

void setup() {
  Serial.begin(115200);

  WiFi.begin(SSID, PASS);
  unsigned long startAttemptTime = millis();

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) { 
    delay(1000);
    Serial.print(".");
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Failed to connect to Wi-Fi");
    while (1);
  } else {
    Serial.println("Connected to Wi-Fi");
  }

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    while (1);
  } else {
    Serial.println("IMU initialized successfully!");
  }

  ArduinoCloud.begin(connectionHandler);
  setCloudVariables();

  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accelerationX, accelerationY, accelerationZ);
  }

  ArduinoCloud.update();

  Serial.print("X: ");
  Serial.print(accelerationX);
  Serial.print(" Y: ");
  Serial.print(accelerationY);
  Serial.print(" Z: ");
  Serial.println(accelerationZ);

  delay(1000);
}

void setCloudVariables() {
  ArduinoCloud.addProperty(accelerationX, READ, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(accelerationY, READ, ON_CHANGE, NULL);
  ArduinoCloud.addProperty(accelerationZ, READ, ON_CHANGE, NULL);
}
