unsigned int delay_time = 40;
unsigned int      steps = 5600;

void initialize_feeder()
{
  pinMode(FEED_STEP, OUTPUT);
  pinMode(FEED_DIR, OUTPUT);

  Serial.println("Done feeder initialization");
}


void move_feeder()
{
  digitalWrite(FEED_DIR, HIGH);
  for (int i=0; i<steps; i++)
  {
    digitalWrite(FEED_STEP, HIGH); 
    delayMicroseconds(delay_time);
    digitalWrite(FEED_STEP, LOW); 
    delayMicroseconds(delay_time);
  }
}


void return_feeder()
{
  digitalWrite(FEED_DIR, LOW);
  for (int i=0; i<steps; i++)
  {
    digitalWrite(FEED_STEP, HIGH); 
    delayMicroseconds(delay_time);
    digitalWrite(FEED_STEP, LOW); 
    delayMicroseconds(delay_time);
  }
}
