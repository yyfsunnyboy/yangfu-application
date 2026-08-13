
#include <Servo.h>

Servo myservo1;

#include <DHT.h>
#define DHTPIN 16
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float getDistance(int trig, int echo){
  digitalWrite(trig, LOW);
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  pinMode(echo, INPUT);
  return (pulseIn(echo, HIGH)/2)/29.1;
}


  int _E8_B7_9D_E9_9B_A2 = 0;
  int _E8_A8_88_E6_99_82a = 0;
  int _E8_A8_88_E6_99_82b = 0;

  void setup()
  {
    Serial.begin(9600);
    pinMode(14,INPUT);
    pinMode(17,OUTPUT);
    pinMode(17,INPUT);
    pinMode(13,OUTPUT);
    pinMode(2,OUTPUT);
    pinMode(3,INPUT);
  dht.begin();
   delay(700);
    myservo1.attach(12,544,2400);
    myservo1.attach(12);
    myservo1.write(90);
  }
  void loop()
  {
    Serial.print((_E8_A8_88_E6_99_82a+String("，")+_E8_A8_88_E6_99_82b+String(";")));
    Serial.print(_E8_B7_9D_E9_9B_A2);
    Serial.println((dht.readTemperature()));
    if ((digitalRead(14)) > 1000) {
      myservo1.write(50);
    }
    if ((digitalRead(14)) < 1000) {
      myservo1.write(130);
    }
    if ((dht.readTemperature()) > 33) {
      myservo1.write(130);
      digitalWrite(17,1);
    }
    // 計時a開始
    if ((digitalRead(17)) == 1) {
      _E8_A8_88_E6_99_82a = (_E8_A8_88_E6_99_82a + 1);
      delay(500);
    }
    // 計時a結束
    if (_E8_A8_88_E6_99_82a > 10) {
      digitalWrite(17,0);
    }
    // 計時b開始
    if ((analogRead(15)) < 650 && _E8_B7_9D_E9_9B_A2 < 30) {
      digitalWrite(13,1);
      delay(200);
      _E8_A8_88_E6_99_82b = (_E8_A8_88_E6_99_82b + 1);
    }
    if (_E8_A8_88_E6_99_82b > 20) {
      digitalWrite(13,0);
      _E8_A8_88_E6_99_82b = 0;
    }
    // 計時b結束
    if ((analogRead(15)) > 650) {
      digitalWrite(13,0);
      _E8_A8_88_E6_99_82b = 0;
    }
    _E8_B7_9D_E9_9B_A2 = (getDistance(2,3));


  }
