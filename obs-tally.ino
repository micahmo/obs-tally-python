#define LED 13

void setup() {
  // Begin listening on the serial port
  Serial.begin(9600);

  // Set the LED pin (13) to output
  pinMode(LED, OUTPUT);
}

void loop() {
  if(Serial.available())
  {
    char currentScene = Serial.read();
    if (currentScene == '1')
    {
      digitalWrite(LED, HIGH);
    }
    else if (currentScene == '2')
    {
      digitalWrite(LED, LOW);
    }
  }
}
