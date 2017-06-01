#define ejeX A0
#define ejeY A1
#define Boton1 2
#define Boton2 3
#define Boton3 4
#define Boton4 5
#define Boton5 6

String DataEjeX;
String DataEjeY;
String A;
String B;
String C;
String D;
String Z;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(ejeX,INPUT);
pinMode(ejeY,INPUT);
pinMode(Boton1,INPUT);
pinMode(Boton2,INPUT);
pinMode(Boton3,INPUT);
pinMode(Boton4,INPUT);
pinMode(Boton5,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  
DataEjeX = 512-(analogRead(ejeX) - 496);
DataEjeY = 512-(analogRead(ejeY)-511);
A = digitalRead(Boton1);
B = digitalRead(Boton2);
C = digitalRead(Boton3);
D = digitalRead(Boton4);
Z = digitalRead(Boton5);

String Data = "{'X' : " + DataEjeX + ", 'Y' : " + DataEjeY + ", 'A': " + A + ", 'B' : " + B + ", 'C' : " + C + ", 'D' : " + D + ", 'Z' : " + Z + "}";

Serial.println(Data);

delay(30);
}
