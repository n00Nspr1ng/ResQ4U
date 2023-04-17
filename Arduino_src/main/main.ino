#define DIR1 2
#define START_STOP1 3
#define SPEED_IN1 A0

//#define DIR2 
//#define START_STOP2 
//#define SPEED_IN2 

void setup()
{
    Serial.begin(9600);

    pinMode(DIR1, OUTPUT);
    pinMode(START_STOP1, OUTPUT);
    pinMode(SPEED_IN1, OUTPUT);

    analogWrite(SPEED_IN1, map(0, 0, 100, 0, 255));

    Serial.println("Initialized.");
    Serial.println("Enter a number between 0 ~ 100.\n");
}

void loop()
{
  if(Serial.available())
  {
    int speed = Serial.parseInt();
    analogWrite(SPEED_IN1, map(speed, 0, 100, 0, 255));

    Serial.print("Spinning at ");
    Serial.println(speed);
  }
  
  delay(20);
}
