#define DIR1 10
#define START_STOP1 11
#define DIR2 12
#define START_STOP2 13

#define SPEED_IN1 5
#define SPEED_IN2 6

bool off_flag;
bool ccw_flag;

void setup()
{
    Serial.begin(19200);

    pinMode(DIR1, OUTPUT);
    pinMode(START_STOP1, OUTPUT);
    pinMode(DIR2, OUTPUT);
    pinMode(START_STOP2, OUTPUT);
    
    pinMode(SPEED_IN1, OUTPUT);
    pinMode(SPEED_IN2, OUTPUT);

    initializeMotor();

    Serial.println("Initialized.");
    Serial.println("Select Mode.");
    Serial.println("1) Speed. 3) Left, Right. 3) On/Off. 4) Dir change. \n");
}

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
        Serial.print("Speed Spinning at ");
        Serial.println(speed);
      }

      Serial.println("\n1) Speed. 2) On/Off. 3) Dir change.");
    }
    else if (mode == 2)
    {
      delay(10);
      Serial.println("Number between 0 ~ 255. \nTo exit enter number -1.");
      while(1)
      {
        while(!Serial.available()){} //wait until serial val is given.
      
        int speed = Serial.parseInt();
        if (speed == -1)
        {
          Serial.println("Exit LR mode.");
          break;
        }
        motorLRControl(speed);
        Serial.print("LR Spinning at ");
        Serial.println(speed);
      }
    }
    else if (mode == 3)
    {
      motorStartStop();
      Serial.print("Motor off_flag: ");
      Serial.println(off_flag);

      Serial.println("\n1) Speed. 2) On/Off. 3) Dir change.");
    }
    else if (mode == 4)
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
