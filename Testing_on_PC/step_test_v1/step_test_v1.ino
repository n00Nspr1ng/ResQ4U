#define STEP 4
#define DIR 5

//steps per revolution 3200

unsigned int delay_time = 40;
unsigned int steps, dir;

void setup() {
  Serial.begin(19200);
  
  pinMode(STEP, OUTPUT);
  pinMode(DIR, OUTPUT);

  Serial.println("Initialized");
  Serial.println("Input: Step, dir");
}

void loop() {
  if (Serial.available())
  {
    steps = Serial.parseInt();
    Serial.print(" Steps: ");
    Serial.println(steps);
    for (int i=0; i<steps; i++)
    {
      digitalWrite(STEP, HIGH); 
      delayMicroseconds(delay_time);
      digitalWrite(STEP, LOW); 
      delayMicroseconds(delay_time);
    }
  }
}
