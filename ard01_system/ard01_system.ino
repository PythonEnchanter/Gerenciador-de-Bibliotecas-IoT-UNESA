#include <DHT.h>

#define KEY 

#define DHTXX 10
#define BUZZER 11
#define TRIG 2
#define ECHO 3
#define BTT1 13
#define BTT2 12
#define RED 8
#define GREEN 7
#define CLEAR 6

DHT dht(DHTXX, DHT11);

int trackZeroDistance = 0;

void setup(){
  Serial.begin(9600);
  
  // Attach the servo to the defined pin
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

  /*buzzerTone(BUZZER, 'R');
  delay(2000);
  delay(2000);
  buzzerTone(BUZZER, ' ');*/

  if (Serial.available() > 0) {
    python = Serial.readStringUntil('\n');

    if(python[0] == 'E'){
      buzzerTone(BUZZER, ' ');
      parseCoordinates(python);
    } else if(python[0] == 'P'){
      buzzerTone(BUZZER, 'S');
      Serial.write("Sistema parado por administrador!");
      delay(30000);
    } else if(python[0] == 'R'){
      buzzerTone(BUZZER, 'R');
      Serial.write("Sistema funcionando normalmente!");
    } else if(python[0] == 'D'){
      //parseCoordinates(python);
      buzzerTone(BUZZER, ' ');
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

  // Example: Print parsed coordinates
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

void pressedButton(){
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
}

void buzzerTone(int buzzerPin, char action){
  //crescente para parada, decrescente para retomada
  int startStopTiming[3] = {500, 500, 2000};
  int startStop[3] = {400, 400, 100};

  int deliveryTiming[] = {500, 500, 500, 500, 250, 50, 50, 2000};
  int delivery[] = {400, 200, 400, 200, 800, 800, 800, 800};

  if(action == 'S'){
    for(int i=0;i<sizeof(startStop)/sizeof(startStop[0]);i++){
      tone(buzzerPin, startStop[i], startStopTiming[i]);
      //Serial.println(startStop[i]);
      delay(500);
    }
  } else if (action == 'R'){
    for(int i=sizeof(startStop)/sizeof(startStop[0]);i>0;i--){
      tone(buzzerPin, startStop[i], startStopTiming[i]);
      //Serial.println(startStop[i]);
      delay(500);
    }
  } else {
    for(int i=0;i<sizeof(delivery)/sizeof(delivery[0]);i++){
      tone(buzzerPin, delivery[i], deliveryTiming[i]);
      Serial.println("Pedido transferido para o sistema interno.");
      delay(500);
    }
  }
}

//liga o led com o padrão exigido ['C': Contínuo, 'P': Piscar]
void turnLedOn(int LEDPin, char action){
  if(action=='C'){
    digitalWrite(LEDPin, HIGH);
  } else {
    digitalWrite(LEDPin, HIGH);
    delay(500);
    digitalWrite(LEDPin, LOW);
    delay(500);
  }
}

void forcedStop(){
  //buzzer avisa 3 segundos
  //garra abre
  //led vermelho liga e rgb pisca
  Serial.println("System freeze! Todas as operações postas em fila.");
}