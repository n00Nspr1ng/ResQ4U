void initializeMotor()
{
  analogWrite(SPEED_IN1, map(0, 0, 100, 0, 255));
  digitalWrite(START_STOP1, HIGH); //stop
  off_flag = HIGH;
}


void motorSpeedControl(int speed)
{
  analogWrite(SPEED_IN1, speed);
}


void motorStartStop()
{
  if (off_flag == HIGH) //if motor is off
  {
    digitalWrite(START_STOP1, LOW);
    off_flag = LOW;
  }
  else //if motor is on
  {
    digitalWrite(START_STOP1, HIGH);
    off_flag = HIGH;
  }
}

void motorDir()
{
    if (ccw_flag == HIGH) //if motor dir is ccw
  {
    digitalWrite(DIR1, LOW);
    ccw_flag = LOW;
  }
  else //if motor dir is cw
  {
    digitalWrite(DIR1, HIGH);
    ccw_flag = HIGH;
  }
}
