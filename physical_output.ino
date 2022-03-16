/*
Name: Ishan Vyas
Course: CPSC 599.88 
Assignment 2: Physical Output - EventTennis
UCID: 30068270
Due Date: March 17th, 2022
*/


#include <Servo.h>

Servo ballServo;  
Servo rightPaddleServo;
Servo leftPaddleServo;

// Keeps track of the ballServo position
int pos = 0;   
// Keeps track of the rightPaddleServo position
int rpos = 115;
// Keeps track of the leftPaddleServo position
int lpos = 105;

// Stores the number of events
int numE;
// Stores the current delay time
int delayTime;

void setup() {
  Serial.begin(9600);           // Begin Serial at 9600
  Serial.setTimeout(1);         // Wait at most 1000ms for serial data
  ballServo.attach(10);         // attaches the ballServo on pin 10 to the servo object
  rightPaddleServo.attach(9);   // attaches the rightPaddleServo on pin 9 to the servo object
  leftPaddleServo.attach(11);   // attaches the leftPaddleServo on pin 11 to the servo object
  // leftPaddleServo.write(110);   // 135 - 75 ==== 105
  // ballServo.write(110);         // 25 - 120 === 35, 115
  // rightPaddleServo.write(55);   // 55 - 85 ==== 120
}

void loop() {
  
  // Check for serial data
  while (!Serial.available());
  // Get serial data from reading the serial port, data sent by python
  numE = Serial.readString().toInt();

  // Map the number of events to a delay time
  if(numE != 0){
    delayTime = 30/numE;
  }else{
    delayTime = 30;
   } 

  // Write the delay time to serial, for output in python
  Serial.print(delayTime);

  // Show the current speed 5 times
  for(int i = 0; i < 5; i += 1){
  
    // Positive Motion
    for (int i = 0; i < 95; i += 1) {
      pos = 120 - i;              
      rpos = 85 - (i/(19/6)); 
      lpos = 135 - (i/(19/5));          

      // Write the positions of the servo
      ballServo.write(pos);
      rightPaddleServo.write(rpos); 
      leftPaddleServo.write(lpos);

      // Dynamic delay time
      delay(delayTime);                          
    }

    // Negative Motion
    for (int i = 0; i < 95; i += 1) {
      pos = 25 + i;              
      rpos = 55 + (i/(19/6));  
      lpos = 110 + (i/(19/5));      

      // Write the positions of the servo
      ballServo.write(pos);
      rightPaddleServo.write(rpos);
      leftPaddleServo.write(lpos); 

      // Dynamic delay time
      delay(delayTime);                          
    }
  }
 
}
