void setup() {
  Serial.begin(9600);
  while (!Serial);  // Wait for serial port to connect
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    int blinkCount = Serial.parseInt();
    Serial.print("Blink count received: ");
    Serial.println(blinkCount);

    for (int i = 0; i < blinkCount; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
    }

    int responseNumber = random(1, 10);
    Serial.print("Response number: ");
    Serial.println(responseNumber);
  }
}
