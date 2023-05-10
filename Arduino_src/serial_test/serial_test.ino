#define LED 7

char a;

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

}

void loop() {
  if (Serial.available()){
    a = Serial.read();

    if (a == 'd') {
      digitalWrite(LED, HIGH);
    }
    else if (a == 'a') {
      digitalWrite(LED, LOW);
    }
  }

}
