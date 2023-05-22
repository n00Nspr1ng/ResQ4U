#include <SoftwareSerial.h>

char flag;
float distance;

bool send_dist_flag = false;

void setup()
{
  // Serial for Raspberry Pi
  Serial.begin(9600); 

  initialize_motor();
  initialize_lidar();
  //initialize_feeder();

  Serial.println("Arduino is ready");
}


void loop()
{

  if (Serial.available())
  { // Read flag from Raspberry Pi
    flag = Serial.read();
  }
  
  // Send flag to Raspberry Pi
  Serial.println(flag);  

  
  if (flag == 'd') //Flag : "detected"
  {
    lidar_loop();
  }
  else if (flag == 'a') //Flag : "aligned"
  {
    if (send_dist_flag == false){
      put_dist_flag();
      send_dist_flag = true;
    }
    lidar_loop();

    float distance = get_final_dist();
    if (distance != 0)
    {
      bldc_control(distance/100.0);
      //feed_control();
      flag = 'e'; //Flag : "end"
    }     
  }
}
