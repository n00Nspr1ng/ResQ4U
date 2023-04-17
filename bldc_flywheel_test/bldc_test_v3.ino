#define DIR1 7
#define START_STOP1 4
#define SPEED_IN1 5

//#define ENC1_A 2
//#define ENC1_B 3

bool off_flag;
bool ccw_flag;

void setup()
{
    Serial.begin(19200);

    pinMode(DIR1, OUTPUT);
    pinMode(START_STOP1, OUTPUT);
    pinMode(SPEED_IN1, OUTPUT);

//    pinMode(ENC1_A, INPUT);
//    pinMode(ENC1_B, INPUT);
//    attachInterrupt(digitalPinToInterrupt(ENC1_A), read_A, CHANGE);
//    attachInterrupt(digitalPinToInterrupt(ENC1_B), read(ENC1_B), CHANGE);

    initializeMotor();

    Serial.println("Initialized.");
    Serial.println("Select Mode.");
    Serial.println("1) Speed. 2) On/Off. 3) Dir change. \n");
}

//void read_A()
//{
//  Serial.print("ENC1_A : ");
//  Serial.println(digitalRead(ENC1_A));
//}

void loop()

{
  if(Serial.available())
  {
    int mode = Serial.parseInt();
    if (mode == 1)
    {
      delay(10);
      Serial.println("Number between 0 ~ 255. \nTo exit enter number -1.");
      while(1)
      {
        while(!Serial.available()){} //wait until serial val is given.
      
        int speed = Serial.parseInt();
        if (speed == -1)
        {
          Serial.println("Exit speed mode.");
          break;
        }
        motorSpeedControl(speed);
        Serial.print("Spinning at ");
        Serial.println(speed);
      }

      Serial.println("\n1) Speed. 2) On/Off. 3) Dir change.");
    }
    else if (mode == 2)
    {
      motorStartStop();
      Serial.print("Motor off_flag: ");
      Serial.println(off_flag);

      Serial.println("\n1) Speed. 2) On/Off. 3) Dir change.");
    }
    else if (mode == 3)
    {
      motorDir();
      Serial.println("Changed direction");

      Serial.println("\n1) Speed. 2) On/Off. 3) Dir change.");
    }
  }

  //Serial.print(digitalRead(ENC1_A));
  //Serial.println(digitalRead(ENC1_B));
  delay(50);
}
