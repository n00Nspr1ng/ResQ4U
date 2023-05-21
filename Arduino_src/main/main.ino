#include <SoftwareSerial.h>

char flag;
float distance;

bool send_dist_flag = false;

void setup()
{
  // Serial for Raspberry Pi
  Serial.begin(9600); 

  //initialize_motor();
  initialize_lidar();
  //initialize_feeder();

  Serial.println("hello");
}


void loop()
{

  if (Serial.available())
  {
    flag = Serial.read();
  }
  Serial.println(flag);

  
  if (flag == 'd') //detected
  {
    lidar_loop();
  }
  else if (flag == 'a') //aligned
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
      flag = 'e';
    }     
  }
}
