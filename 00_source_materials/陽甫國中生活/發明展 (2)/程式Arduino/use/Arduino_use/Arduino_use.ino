#include <SoftwareSerial.h>
#include <Servo.h>
#include <DHT.h>

#define DHTTYPE DHT11

int timing_a = (int)(0);
int timing_b = (int)(0);
char CHAR = (char)(0);
int distance = (int)(0);
int temperature = (int)(0);
Servo servo_9;

SoftwareSerial BT(10, 11); //藍芽端接收腳對應Arduino傳送腳, 藍芽端傳送腳對應Arduino接收腳
DHT dht6(6, DHTTYPE);


float ultrasonic_distance_cm(int trigPin, int echoPin){
  digitalWrite(trigPin, LOW);
  digitalWrite(echoPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  unsigned long sonic_duration = pulseIn(echoPin, HIGH);
  float distance_cm = (sonic_duration / 2.0) / 29.1;

  return distance_cm;
}

// 自動化運行: 花園
void automation___garden() {
  if (temperature > 30) {
    servo_9.write(155);
    digitalWrite(4, HIGH);
  } else {
    servo_9.write(110);
    digitalWrite(4, LOW);
    delay(1000);
  }
  if (analogRead(A5) < 650 && distance < 20) {
    digitalWrite(5, HIGH);
  } else {
    digitalWrite(5, LOW);
    delay(1000);
  }
}

// 自動化運行: 曬衣
void automation___drying_clothes() {
  if (analogRead(A0) < 1000) {
    servo_9.write(155);
  } else if (analogRead(A0) > 1000) {
    servo_9.write(110);
  }
  if (analogRead(A5) < 650 && distance < 20) {
    digitalWrite(5, HIGH);
  } else {
    digitalWrite(5, LOW);
    delay(1000);
  }
}

// 自動化運行: 看護
void automation___take_care_of() {
  if (analogRead(A0) < 1000) {
    servo_9.write(155);
  } else if (analogRead(A0) > 1000) {
    servo_9.write(110);
  }
  if (temperature > 26) {
    servo_9.write(155);
    digitalWrite(4, HIGH);
  } else {
    digitalWrite(4, LOW);
    delay(1000);
  }
  if (analogRead(A5) < 650 && distance < 20) {
    digitalWrite(5, HIGH);
  } else {
    digitalWrite(5, LOW);
    delay(1000);
  }
}

// 描述此函數...
void CLOSE_LIGHT() {
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(12, LOW);
}


void setup() {
  BT.begin(9600);
  Serial.begin(9600);
  pinMode(8, OUTPUT);
  pinMode(9, INPUT);
  dht6.begin();
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(A5, INPUT);
  pinMode(A0, INPUT);

  servo_9.attach(7);
  servo_9.write(110);

}

void loop() {
  Serial.println(distance);
  Serial.println(temperature);
  distance = ultrasonic_distance_cm(8, 9);
  temperature = dht6.readTemperature();
  if (BT.available()) {
    CHAR = BT.read();
    Serial.println(CHAR);
  }
  if (CHAR == 'A') {
    automation___drying_clothes();
    digitalWrite(2, HIGH);
    digitalWrite(3, LOW);
    digitalWrite(12, LOW);
  } else if (CHAR == 'B') {
    automation___take_care_of();
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    digitalWrite(12, LOW);
  } else if (CHAR == 'C') {
    automation___garden();
    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(12, HIGH);
  } else if (CHAR == 'D') {
    servo_9.write(155);
    digitalWrite(5, LOW);
    digitalWrite(4, LOW);
    CLOSE_LIGHT();
  } else if (CHAR == 'E') {
    servo_9.write(155);
    digitalWrite(5, HIGH);
    digitalWrite(4, LOW);
    CLOSE_LIGHT();
  } else if (CHAR == 'F') {
    servo_9.write(155);
    digitalWrite(5, HIGH);
    digitalWrite(4, HIGH);
    CLOSE_LIGHT();
  } else if (CHAR == 'G') {
    servo_9.write(110);
    digitalWrite(5, HIGH);
    digitalWrite(4, LOW);
    CLOSE_LIGHT();
  } else if (CHAR == 'H') {
    servo_9.write(110);
    digitalWrite(5, HIGH);
    digitalWrite(4, HIGH);
    CLOSE_LIGHT();
  } else if (CHAR == 'I') {
    servo_9.write(155);
    digitalWrite(5, LOW);
    digitalWrite(4, HIGH);
    CLOSE_LIGHT();
  } else if (CHAR == 'J') {
    servo_9.write(110);
    digitalWrite(5, LOW);
    digitalWrite(4, HIGH);
    CLOSE_LIGHT();
  } else if (CHAR == 'K') {
    servo_9.write(110);
    digitalWrite(5, LOW);
    digitalWrite(4, LOW);
    CLOSE_LIGHT();
  }

}
