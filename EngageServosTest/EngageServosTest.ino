#include <Servo.h>

#define CLAW 13
#define XSERV 12
#define YSERV 11
#define SIGNALX 8
#define SIGNALY 7

Servo servo, xServo, yServo;
int openAngle = 90;
int closedAngle = 180;

void setup(){
  pinMode(SIGNALX, OUTPUT);
  pinMode(SIGNALY, OUTPUT);
  servo.attach(CLAW);
  xServo.attach(XSERV);
  yServo.attach(YSERV);
}

void loop(){c:\Users\berna_iy46ate\Documents\GitHub\Gerenciador-de-Bibliotecas-IoT-UNESA\ard01_system\ard01_system.ino
  /*openClaw(servo);
  delay(3000);
  closeClaw(servo);
  delay(3000);*/

  engageServo(xServo, SIGNALX);
}

void openClaw(Servo servo){
  servo.write(openAngle);
}

void closeClaw(Servo servo){
  servo.write(closedAngle);
}

void engageServo(Servo servo, int signalPin){
  digitalWrite(signalPin, HIGH);
  servo.write(90);
}