#define ejeX A0
#define ejeY A1

String DataEjeX = "";
String DataEjeY = "";

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
String Data = "{'X' : " + DataEjeX + ", 'Y' : " + DataEjeY + "}";

Serial.println(Data);

delay(30);
}
