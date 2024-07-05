// Pin definitions
const int DIR_A = 7;   // Direction pin for motor A
const int PWM_A = 6;   // PWM pin for motor A
const int DIR_B = 8;   // Direction pin for motor B
const int PWM_B = 9;   // PWM pin for motor B

void setup() {
  // Set direction pins as outputs
  pinMode(DIR_A, OUTPUT);
  pinMode(DIR_B, OUTPUT);
  
  // Set PWM pins as outputs
  pinMode(PWM_A, OUTPUT);
  pinMode(PWM_B, OUTPUT);
}

void loop() {
  //low = forward
  // Set motors to move forward
  digitalWrite(DIR_A, LOW);
  digitalWrite(DIR_B, LOW);
  
  // Run motors at 50% speed
  analogWrite(PWM_A, 100);
  analogWrite(PWM_B, 100);
  
  // Run motors for 5 seconds
  delay(5000);

  for(int i=100;i>=0;i--)
  {
    analogWrite(PWM_A, 100);
    analogWrite(PWM_B, i);     
    delay(50); 
  }
  // Stop motors
  analogWrite(PWM_A, 0);
  analogWrite(PWM_B, 0);
  
  // Wait for 5 seconds before running again
  delay(5000);
}
