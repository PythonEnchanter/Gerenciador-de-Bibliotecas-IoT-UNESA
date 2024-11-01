#include <Servo.h>
#include <DHT.h>

// Define the pinS for each sensor
#define CLAW 8
#define DHT11 13
#define BUZZER 5
#define SOUND1 12 
#define SOUND2 11
#define BTT1 7
#define BTT2 6

// Create a Servo object
Servo clawServo;
DHT dht();

// Define angles for open and close positions
const int openAngle = 90;   
const int closeAngle = 170;

void changeClaw();
void forcedStop();

void setup(){
  Serial.begin(9600);
  
  // Attach the servo to the defined pin
  pinMode(DHT11, OUTPUT);
  pinMode(SOUND1, OUTPUT);
  pinMode(SOUND2, OUTPUT);
  pinMode(BTT1, OUTPUT);
  pinMode(BTT2, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  clawServo.attach(CLAW); claw_state = 0;
  clawServo.changeClaw();
}

void loop(){

}

void pressedButton1(){

}

void retrieveHumidity(){
  //puxa os dados de humidade do sensor DHT11
}

void retrieveTemperature(){
  //puxa os dados de humidade do sensor DHT11
}

void forcedStop(){
  //buzzer avisa 3 segundos
  //garra abre
  //led vermelho liga e rgb pisca
}

void changeClaw(){
  if(claw_state == 1){
    servo.write(openAngle);
    claw_state = 0
  } else servo.write(closeAngle);
}