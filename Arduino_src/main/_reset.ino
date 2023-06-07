void initialize_arduino()
{
  digitalWrite(RESET, HIGH);
  delay(200);
  pinMode(RESET, OUTPUT);
}

void reset_arduino()
{
  Serial.println("Resetting Arduino ...");
  digitalWrite(Reset, LOW);
}
