#include <SoftwareSerial.h>

char flag;
float distance;

bool send_align_flag = false;

void setup()
{
  // Serial for Raspberry Pi
  Serial.begin(9600); 
  initialize_arduino();
  
  initialize_bldc();
  initialize_lidar();
  initialize_feeder();

  Serial.println("Arduino is ready");
}


void loop()
{

  if (Serial.available())
  { // Read flag from Raspberry Pi
    flag = Serial.read();
  }
  
  // Send flag to Raspberry Pi
  //Serial.println(flag);  

  
  if (flag == 'd') //Flag : "detected"
  {
    lidar_loop();
  }
  else if (flag == 'a') //Flag : "aligned"
  {
    if (send_align_flag == false){
      put_align_flag();
      send_align_flag = true;
    }
    lidar_loop();

    float distance = get_final_dist();
    if (distance != 0)
    {
      bldc_control(distance/100.0);
      delay(4000);
      
      flag = 'f'; //Flag : "feeder"
    }     
  }
  else if (flag == 'f') //Flag: "feeder"
  {  
    move_feeder();
    delay(3000);
    
    flag = 'e';
  }
  else if (flag == 'e') //Flag : "ended"
  {
    turn_off_motor();
    return_feeder();

    //Send flag to Raspberry Pi
    Serial.println("Arduino Ended");
    
    //Reset Arduino
    reset_arduino();
  }
}
