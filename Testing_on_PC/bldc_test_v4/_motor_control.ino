void initializeMotor()
{
  analogWrite(SPEED_IN1, 0);
  analogWrite(SPEED_IN2, 125);
  digitalWrite(START_STOP1, HIGH); //stop
  digitalWrite(START_STOP2, HIGH); //stop
  off_flag = HIGH;
}


void motorSpeedControl(int speed)
{
  analogWrite(SPEED_IN1, speed);
}


void motorLRControl(int speed)
{
  analogWrite(SPEED_IN2, speed);
}


void motorStartStop()
{
  if (off_flag == HIGH) //if motor is off
  {
    digitalWrite(START_STOP1, LOW);
    digitalWrite(START_STOP2, LOW);
    off_flag = LOW;
  }
  else //if motor is on
  {
    digitalWrite(START_STOP1, HIGH);
    digitalWrite(START_STOP2, HIGH);
    off_flag = HIGH;
  }
}


void motorDir()
{
    if (ccw_flag == HIGH) //if motor dir is ccw
  {
    digitalWrite(DIR1, LOW);
    digitalWrite(DIR2, LOW);
    ccw_flag = LOW;
  }
  else //if motor dir is cw
  {
    digitalWrite(DIR1, HIGH);
    digitalWrite(DIR2, HIGH);
    ccw_flag = HIGH;
  }
}
