#include <Keypad.h>
#include <Adafruit_LiquidCrystal.h>

const byte LINHAS = 4;
const byte COLUNAS = 4;
byte tcldLinha[4] = {9, 8, 7, 6};
byte tcldColuna[4] = {5, 4, 3, 2};
char teclas[LINHAS][COLUNAS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

//Inicializa o display LCD
Adafruit_LiquidCrystal lcdDisplay(0);

Keypad teclado = Keypad(makeKeymap(teclas), tcldLinha, tcldColuna, LINHAS, COLUNAS);

void setup(){
  lcdDisplay.begin(16, 2); //São 2 linhas de 16 caracteres cada
  lcdDisplay.print("Seja bem-vindo!");
  lcdDisplay.setCursor(0, 1);
  lcdDisplay.print("Biblioteca UNESA");
  Serial.begin(9600);
  
  delay(5000);
  clearDisplayLine(1);
  
  //teclado matricial
  for(int i=0;i<4;i++){
    pinMode(tcldLinha[i], OUTPUT);
    digitalWrite(tcldLinha[i], LOW);
    pinMode(tcldColuna[i], INPUT_PULLUP);
  }
}

void loop(){ //separar a função do clique
  lcdDisplay.setCursor(entrySenha(), 1);
}

//Recebe a senha do usuário
int entrySenha(){
  int pos = 0;
  int senha[6] = {};

  lcdDisplay.setCursor(0, 1);
  while(pos < 6){
    char tecla = teclado.getKey();
    if(tecla){ // Verifica se uma tecla foi pressionada
      Serial.print((String)"YAY " + tecla + pos);
      lcdDisplay.print("*"); // Imprime a tecla pressionada

      // Verifica se a tecla é um número entre '0' e '9'
      if (tecla >= 48 && tecla <= 57){
        senha[pos] = tecla;
        pos++;

        if (pos == 6) {
          senha[6] = '\0';

          return 6;
        }
      }
    }
  }
  
  return pos;
}

//limpa uma linha inteira do display
void clearDisplayLine(int line){
  for(int i=0;i<16;i++){
    lcdDisplay.setCursor(i, line);
    lcdDisplay.print(" ");
  } lcdDisplay.setCursor(0, line);
}
