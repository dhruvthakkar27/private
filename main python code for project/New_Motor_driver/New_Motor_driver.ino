// Define pin connections
const int RPWM = 5;
const int LPWM = 6;
const int REN = 7;
const int LEN = 8;
const int EN= 9;


void setup() {
  // Set pins as outputs
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(REN, OUTPUT);
  pinMode(LEN, OUTPUT);
  pinMode(EN, OUTPUT);
  Serial.begin(9600);
  // Enable motor driver
  digitalWrite(REN, HIGH);
  digitalWrite(LEN, HIGH);
}

void loop() {
  // Drive forward
 
  digitalWrite(EN,LOW);
  Serial.println("FW");
  digitalWrite(REN,HIGH);
  digitalWrite(LEN,HIGH);
  analogWrite(RPWM, 255); // Full speed
  analogWrite(LPWM, 0);
  delay(5000); // 5 seconds

  // Stop motor
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  delay(1000); // 1 second pause to avoid abrupt direction change
 
//  // Drive reverse
  digitalWrite(EN,HIGH);
  Serial.println("rev");
  analogWrite(LPWM, 0);
  analogWrite(RPWM, 255); // Full speed
  delay(5000); // 5 seconds
//
//  // Stop motor
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  delay(1000); // 1 second pause to avoid abrupt direction change
}
