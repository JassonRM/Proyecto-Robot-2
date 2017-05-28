#define ejeX A0
#define ejeY A1
#define Boton1 2
#define Boton2 3
#define Boton3 4
#define Boton4 5

String DataEjeX;
String DataEjeY;
String A;
String B;
String C;
String D;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(ejeX,INPUT);
pinMode(ejeY,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
DataEjeX = analogRead(ejeX);
DataEjeY = analogRead(ejeY);
A = digitalRead(Boton1);
B = digitalRead(Boton2);
C = digitalRead(Boton3);
D = digitalRead(Boton4);

String Data = "{'X' : " + DataEjeX + ", 'Y' : " + DataEjeY + ", 'A ': " + A + ", 'B' : " + B + ", 'C' : " + C + ", 'D' : " + D + "}";

Serial.println(Data);

delay(30);
}
