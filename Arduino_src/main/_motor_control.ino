float speed_dist_chart[10][2] = {{170.0, 1.97},
                                  {175.0, 2.97},
                                  {180.0, 4.10},
                                  {185.0, 5.57},
                                  {190.0, 7.47},
                                  {195.0, 9.10},
                                  {200.0, 11.23},
                                  {205.0, 13.13},
                                  {210.0, 13.87},
                                  {215.0, 13.9}};

int current_speed;

void initialize_bldc()
{
  pinMode(DIR1, OUTPUT);
  pinMode(START_STOP1, OUTPUT);
  pinMode(DIR2, OUTPUT);
  pinMode(START_STOP2, OUTPUT);
    
  pinMode(SPEED_IN1, OUTPUT);
  pinMode(SPEED_IN2, OUTPUT);

  analogWrite(SPEED_IN1, 125);
  analogWrite(SPEED_IN2, 125);
  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);
  digitalWrite(START_STOP1, HIGH); //stop
  digitalWrite(START_STOP2, HIGH); //stop

  Serial.println("Done BLDC initialization");

}

void bldc_control(float distance)
{
  Serial.print("got ");
  Serial.println(distance);
  int speed = get_speed(distance);
  Serial.print("Speed = ");
  Serial.println(speed);
  current_speed = speed;

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
    Serial.println("ff");
    analogWrite(SPEED_IN1, 150);
    delay(250);
    analogWrite(SPEED_IN1, 170);
    delay(250);
    analogWrite(SPEED_IN1, speed);
  }
  else if (speed < 210)
  {
    analogWrite(SPEED_IN1, 150);
    delay(250);
    analogWrite(SPEED_IN1, 170);
    delay(250);
    analogWrite(SPEED_IN1, 190);
    delay(250);
    analogWrite(SPEED_IN1, speed);
  }
}

void turn_off_motor()
{
  Serial.print("current speed at");
  Serial.println(current_speed);
  
  // Slowly decrease motor speed
  if (current_speed < 170)
  {
    analogWrite(SPEED_IN1, 150);
    delay(250);
    analogWrite(SPEED_IN1, 125);
  }
  else if (current_speed < 190)
  {
    analogWrite(SPEED_IN1, 170);
    delay(250);
    analogWrite(SPEED_IN1, 150);
    delay(250);
    analogWrite(SPEED_IN1, 125);
  }
  else if (current_speed < 210)
  {
    analogWrite(SPEED_IN1, 190);
    delay(250);
    analogWrite(SPEED_IN1, 170);
    delay(250);
    analogWrite(SPEED_IN1, 150);
    delay(250);
    analogWrite(SPEED_IN1, 125);
  }

  // Turn motor off
  digitalWrite(START_STOP1, HIGH);
  digitalWrite(START_STOP2, HIGH);

}


int get_speed(float distance)
{
  int min_index = 0;
  float min_dist = distance - speed_dist_chart[min_index][1];
  float temp;
  for (int i=1; i<10; i++)
  {
    temp = distance - speed_dist_chart[i][1];
    
    if (temp < 0)
      break;  
    
    min_dist = temp;
    min_index = i;
  }
  Serial.print("min_index = ");
  Serial.println(speed_dist_chart[min_index][0]);

  int bldc_input;
  if (temp = 0 || min_index == 9)
    bldc_input = speed_dist_chart[min_index][0];
  else
    bldc_input = round(speed_dist_chart[min_index][0] + (speed_dist_chart[min_index + 1][0] - speed_dist_chart[min_index][0])/(speed_dist_chart[min_index + 1][1] - speed_dist_chart[min_index][1])*(distance - speed_dist_chart[min_index][1]));

  return bldc_input;
}
