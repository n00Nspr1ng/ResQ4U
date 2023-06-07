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

  Serial.println("BLDC Initialization Done");

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
  for (int i = 150; i <= speed; i += 5) {
    analogWrite(SPEED_IN1, i);
    delay(200);
  }
}

void turn_off_motor()
{
  Serial.print("current speed at");
  Serial.println(current_speed);
  // Slowly decrease motor speed
  for (int i = current_speed; i >= 150; i -= 5) {
    analogWrite(SPEED_IN1, i);
    delay(250);
  }
  // Turn motor off
  digitalWrite(START_STOP1, HIGH);
  digitalWrite(START_STOP2, HIGH);
}


int get_speed(float distance)
{
  int low = 0;
  int high = 9;
  int mid;
  
  while (low <= high){
    mid = (low + high) / 2;
    if (speed_dist_chart[mid][1] < distance)
      low = mid + 1;
    else if (speed_dist_chart[mid][1] > distance)
      high = mid - 1;
    else
      return speed_dist_chart[mid][0];
  }
  
  // Find 2 closest distances (high & low)
  int index1 = high;
  int index2 = low;
  
  // Interpolate distances from chart
  float dist1 = speed_dist_chart[index1][1];
  float dist2 = speed_dist_chart[index2][1];
  float ratio = (distance - dist1) / (dist2 - dist1);
  
  int speed1 = speed_dist_chart[index1][0];
  int speed2 = speed_dist_chart[index2][0];
  int bldc_input = round(speed1 + ratio * (speed2 - speed1));
  
  return bldc_input;
}
