double speed_dist_chart[10][2] = {{170.0, 1.97},
                                  {175.0, 2.97},
                                  {180.0, 4.10},
                                  {185.0, 5.57},
                                  {190.0, 7.47},
                                  {195.0, 9.10},
                                  {200.0, 11.23},
                                  {205.0, 13.13},
                                  {210.0, 13.87},
                                  {215.0, 13.9}};


void initialize_motor()
{
  analogWrite(SPEED_IN1, 125);
  analogWrite(SPEED_IN2, 125);
  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  digitalWrite(START_STOP1, HIGH); //stop
  digitalWrite(START_STOP2, HIGH); //stop
  //off_flag = HIGH;
}


void bldc_control(int distance)
{
  int speed = get_speed(distance);
  Serial.print("Speed = ")
  Serial.println(speed)

  // Turn motor on
  digitalWrite(START_STOP1, LOW);
  digitalWrite(START_STOP2, LOW);

  // Slowly increase motor speed
  if (speed < 170)
  {
    analogWrite(SPEED_IN1, 150);
    delay(50);
    analogWrite(SPEED_IN1, speed);
  }
  else if (speed < 190)
  {
    analogWrite(SPEED_IN1, 150);
    delay(50);
    analogWrite(SPEED_IN1, 170);
    delay(50);
    analogWrite(SPEED_IN1, speed);
  }
  else if (speed < 210)
  {
    analogWrite(SPEED_IN1, 150);
    delay(50);
    analogWrite(SPEED_IN1, 170);
    delay(50);
    analogWrite(SPEED_IN1, 190);
    delay(50);
    analogWrite(SPEED_IN1, speed);
  }
}


int get_speed(int distance)
{
  int min_index = 0;
  int min_dist = distance - speed_dist_chart[min_index][1];
  int temp;
  for (int i=1; i<10; i++)
  {
    temp = distance - speed_dist_chart[i][1];
    
    if (temp < 0)
      break;  
    
    min_dist = temp;
    min_index = i;
  }

  if (temp = 0 || min_index == 9)
    return speed_dist_chart[min_index][0]
  else
  {
    int speed = round(speed_dist_chart[min_index][0] + (speed_dist_chart[min_index + 1][0] - speed_dist_chart[min_index][0])/(speed_dist_chart[min_index + 1][1] - speed_dist_chart[min_index][1])*(distance - speed_dist_chart[min_index][1]))
    return speed
  }
}


//////////////////////////// Deprecated ////////////////////////////
void bldcSpeedControl(int speed)
{
  analogWrite(SPEED_IN1, speed)
}

void bldcLRControl(int speed)
{
  analogWrite(SPEED_IN2, speed);
}

void bldcStartStop()
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

void bldcDir()
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
    digitalWrite(DIR2, LOW);
    ccw_flag = HIGH;
  }
}
