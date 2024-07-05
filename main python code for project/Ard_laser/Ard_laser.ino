const int inputPin = 2;  // Pin connected to the Coral output
const int ledPin = 13;   // Pin connected to the LED

void setup() {
  pinMode(inputPin, INPUT);   // Set the input pin as input
  pinMode(ledPin, OUTPUT);    // Set the LED pin as output
}

void loop() {
  // Read the state of the input pin
  int inputState = digitalRead(inputPin);
  
  // Turn on or off the LED based on the input state
  if (inputState == HIGH) {
    digitalWrite(ledPin, LOW);  // Turn on the LED
  } else {
    digitalWrite(ledPin, HIGH);   // Turn off the LED
  }
}
