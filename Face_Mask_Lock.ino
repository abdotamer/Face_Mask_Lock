#include<Servo.h>
Servo lock;
void setup() {
    Serial.begin(9600);
    lock.attach(9);
    lock.write(0);
}

void loop() {
  if(Serial.available())
  {
    int x = Serial.readStringUntil('\r\n').toInt();
    if(x == 0)
    {
      lock.write(0);
    }
    else
    {
      lock.write(90);
    }
  }
}
