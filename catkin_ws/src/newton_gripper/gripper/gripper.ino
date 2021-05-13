#include <Servo.h>

#define GRIPPER_PWM_PIN 9
#define LEFT 12 // PIN 2 IS CONNECTED TO LEFT BUTTON      
#define RIGHT 2 // PIN 2 IS CONNECTED TO RIGHT BUTTON 

#define OPEN_PWM_US       1100  // Gripper open PWM output (us)
#define CLOSE_PWM_US      1900  // Gripper close PWM output (us)
#define STOP_PWM_US       1500 // Gripper stop PWM output (us)

int buttonState1 = 0;
int buttonState2 = 0;

Servo gripper;

void setup() 
{
  Serial.begin(9600);
  gripper.attach(GRIPPER_PWM_PIN);
  pinMode(LEFT, INPUT_PULLUP); // assign pin 12 ass input for Left button
  pinMode(RIGHT, INPUT_PULLUP); // assing pin 2 as input for right button
}


void loop()
{
  buttonState1 = digitalRead(RIGHT);
  buttonState2 = digitalRead(LEFT);

  if (buttonState1 == LOW)
  {
    Serial.println("bottom button - opening");
    gripper.writeMicroseconds(OPEN_PWM_US);
  }
  else if (buttonState2 == LOW)
  {
    Serial.println("top button - closing");
    gripper.writeMicroseconds(CLOSE_PWM_US);
  }
  else
  {
    gripper.writeMicroseconds(STOP_PWM_US); 
  } 
}