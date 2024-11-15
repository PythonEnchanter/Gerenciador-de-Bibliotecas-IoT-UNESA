#include <DHT.h>

#define KEY 

#define DHTXX 10
#define BUZZER 11
#define TRIG 2
#define ECHO 3
#define BTT1 9
#define BTT2 12
#define RED 8
#define GREEN 7
#define CLEAR 6

DHT dht(DHTXX, DHT11);

//ambient variables
int trackZeroDistance = 0;
int stopButtonPress = 0;
int restartButtonPress = 0;
String systemStatus = "active";

void setup(){
  Serial.begin(9600);
  
  pinMode(DHT11, OUTPUT);
  pinMode(TRIG, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(BTT1, INPUT);
  pinMode(BTT2, INPUT);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(CLEAR, OUTPUT);

  dht.begin();
}

void loop(){
  String python = "";
  stopButtonPress = digitalRead(BTT2);
  restartButtonPress = digitalRead(BTT1);

  //pressedButton('R');

  if(stopButtonPress == HIGH && systemStatus == "active"){
    pressedButton('S');
    delay(50);
  } else if(restartButtonPress == HIGH && systemStatus == "inactive"){
    pressedButton('R');
    systemStatus = "active";
    delay(50);
  }

  if (Serial.available() > 0) {
    python = Serial.readStringUntil('\n');
    
    if(python[0] == 'E'){
      buzzerTone(BUZZER, ' ');
      parseCoordinates(python);
      if(checkBookPresence()){
        Serial.print("Pedido transferido para o sistema interno.");
      delay(100);
      } else Serial.print("Aguarde mais alguns instantes!");
    } else if(python[0] == 'P'){
      //buzzerTone(BUZZER, 'S');
      Serial.print("Sistema parado por administrador!");
      delay(100);
      delay(30000);
    } else if(python[0] == 'R'){
      //buzzerTone(BUZZER, 'R');
      Serial.print("Sistema funcionando normalmente!");
      delay(100);
    } else if(python[0] == 'D'){
      buzzerTone(BUZZER, ' ');
      Serial.print("Livros devolvidos!");
    } else if(python[0] == 'I'){
      String internalInfo = "Temp: " + String(retrieveTemperature()) + " " + "Hum: " + String(retrieveHumidity());
      Serial.print(internalInfo);
    }
  }
}

void parseCoordinates(String data){
  /*int coordIndex = 0;
  int startIndex = 0;
  int commaIndex, semiColonIndex;

  while (startIndex < data.length()) {
    commaIndex = data.indexOf(',', startIndex);
    semiColonIndex = data.indexOf(';', startIndex);

    if (commaIndex == -1 || semiColonIndex == -1) break;

    int x = data.substring(startIndex, commaIndex).toInt();
    int y = data.substring(commaIndex + 1, semiColonIndex).toInt();


    if (coordIndex < 10){
      coordinates[coordIndex][0] = x;
      coordinates[coordIndex][1] = y;
      coordIndex++;
    }

    startIndex = semiColonIndex + 1;
  }


  for (int i = 0; i < coordIndex; i++) {
    Serial.print("X: ");
    Serial.print(coordinates[i][0]);
    Serial.print(", Y: ");
    Serial.println(coordinates[i][1]);
  }*/
}

//verifica se o livro está sendo levado pela esteira
bool checkBookPresence(){
  trackZeroDistance = soundSensor(TRIG, ECHO);  // Distância inicial ao chão
  unsigned long timer = millis();

  Serial.println("Distância Inicial: " + String(trackZeroDistance) + " cm");

  // Verifica continuamente se há uma alteração na distância
  while(true) {
    int currentDistance = soundSensor(TRIG, ECHO);
    Serial.println("Distância Atual: " + String(currentDistance) + " cm");
    
    // Verifica se a distância diminuiu, indicando um objeto
    if (currentDistance < trackZeroDistance-5){
      Serial.println("Objeto detectado! Distância inferior à inicial.");
      return true;  // Objeto detectado
    }

    if((millis() - timer) > 30000) {
      Serial.println("Timeout: Nenhum objeto detectado. Finalizando...");
      return false;
    }

    delay(500);  //Pequeno atraso entre leituras para evitar sobrecarga
  }
}

int soundSensor(int trig,int echo){
  digitalWrite(trig,LOW);
  delayMicroseconds(2);
  digitalWrite(trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(trig,LOW);

  return pulseIn(echo, HIGH)/58;
}

void pressedButton(char btt){
  if(btt == 'S'){
      forcedStop();
  } else {
    returnAction();
  }
}

float retrieveHumidity(){
  //puxa os dados de humidade do sensor DHT11
  return dht.readHumidity();
}

float retrieveTemperature(){
  //puxa os dados de temperatura do sensor DHT11
  return dht.readTemperature();
}

void returnAction(){
  //buzzer avisa 1 segundo
  //led verde pisca 3 vezes e rbg desliga
  //as ações travadas voltam em fila
  //buzzerTone(BUZZER, 'R');
  turnLedOn(GREEN, 'P');
  turnLedOn(GREEN, 'C');
  turnLedOn(CLEAR, 'C');
  Serial.println("Sistema em funcionamento! Operações em fila serão executadas.");
}

//S - Stop; R - Restart;
void buzzerTone(int buzzerPin, char action){
  //crescente para parada, decrescente para retomada
  int startStopTiming[3] = {500, 500, 1000};
  int startStop[3] = {400, 400, 100};

  int deliveryTiming[] = {500, 500, 500, 500, 250, 50, 50, 1000};
  int delivery[] = {400, 200, 400, 200, 800, 800, 800, 800};

  if(action == 'S'){
    for(int i=0;i<sizeof(startStop)/sizeof(startStop[0]);i++){
      tone(buzzerPin, startStop[i], startStopTiming[i]);
      delay(500);
    }
  } else if (action == 'R'){
    for(int i=sizeof(startStop)/sizeof(startStop[0]);i>0;i--){
      tone(buzzerPin, startStop[i], startStopTiming[i]);
      delay(500);
    }
  } else {
    for(int i=0;i<sizeof(delivery)/sizeof(delivery[0]);i++){
      tone(buzzerPin, delivery[i], deliveryTiming[i]);
      delay(500);
    }
  }
}

//liga o led com o padrão exigido ['C': Contínuo, 'P': Piscar]
void turnLedOn(int LEDPin, char action){
  if(action=='C'){
    digitalWrite(LEDPin, HIGH);
    delay(50);
  } else{
    for(int i=0;i<3;i++){
      digitalWrite(LEDPin, HIGH);
      delay(50);
      digitalWrite(LEDPin, LOW);
      delay(50);
    }
  }
}

void forcedStop(){
  //buzzer avisa 3 segundos
  //led vermelho liga e rgb pisca
  //buzzerTone(BUZZER, 'S');
  Serial.println("System freeze! Todas as operações postas em fila.");

  while(restartButtonPress == LOW){
    delay(10);
  }
}