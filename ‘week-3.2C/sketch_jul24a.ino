#include "thingProperties.h"
#include <Arduino_LSM6DS3.h>
void setup() {
 Serial.begin(9600);
 if (!IMU.begin()) {
 Serial.println("Failed to initialize IMU!");
 while (1);
 }
 initProperties();
 ArduinoCloud.begin(ArduinoIoTPreferredConnection);
}
void loop() {
 ArduinoCloud.update();
 float x, y, z;
 if (IMU.accelerationAvailable()) {
 IMU.readAcceleration(x, y, z);
 accelerationX = x;
 accelerationY = y;
 accelerationZ = z;
 Serial.print("X: ");
 Serial.print(x);
 Serial.print(" Y: ");
 Serial.print(y);
 Serial.print(" Z: ");
 Serial.println(z);
 if (x > 1.0 || y > 1.0 || z > 1.0) {
 alarm = true;
 } else {
 alarm = false;
 }
 }
}
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>
#include "arduino_secrets.h"
const char SSID[] = SECRET_SSID;
const char PASS[] = SECRET_OPTIONAL_PASS;
float accelerationX;
float accelerationY;
float accelerationZ;
bool alarm;
void initProperties() {
 ArduinoCloud.setThingId("your-thing-id");
 ArduinoCloud.addProperty(accelerationX, READ, ON_CHANGE, NULL);
 ArduinoCloud.addProperty(accelerationY, READ, ON_CHANGE, NULL);
 ArduinoCloud.addProperty(accelerationZ, READ, ON_CHANGE, NULL);
 ArduinoCloud.addProperty(alarm, READWRITE, ON_CHANGE, NULL);
}
WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);