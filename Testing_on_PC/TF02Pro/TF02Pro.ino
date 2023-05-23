// soft serial port header file
#include<SoftwareSerial.h>

// define the soft serial port as Serial1, pin2 as RX, and pin3 as TX
// pin 2 - Green, pin 3 - White
SoftwareSerial Serial1(2,3);


int dist;// LiDAR actually measured distance value
int strength;// LiDAR signal strength
int check;// check numerical value storage
int i;

int uart[9];// store data measured by LiDAR
const int HEADER=0x59;// data package frame header

void setup()
{
  Serial.begin(19200);//set the Baud rate of Arduino and computer serial port
  Serial1.begin(115200);//set the Baud rate of LiDAR and Arduino serial port

  Serial.println("Initialized");
}

// main loop
void loop()
{
  if (Serial1.available())//check whether the serial port has data input
  {
    if(Serial1.read()==HEADER)// determine data package frame header 0x59
    {
      uart[0]=HEADER;
      if(Serial1.read()==HEADER)//determine data package frame header 0x59
      {
        uart[1]=HEADER;
        for(i=2;i<9;i++)// store data to array
        {
          uart[i]=Serial1.read();
        }
        check=uart[0]+uart[1]+uart[2]+uart[3]+uart[4]+uart[5]+uart[6]+uart[7];
        if(uart[8]==(check&0xff))// check the received data as per protocols
        {
          dist=uart[2]+uart[3]*256;// calculate distance value -- need check ( in CENTIMETERS )
          strength=uart[4]+uart[5]*256;// calculate signal strength value -- need check
          if (strength >= 0)
          {
            //Serial.print("distance = ");
            Serial.print(dist);// output LiDAR tests distance value
            //Serial.print("cm");
            Serial.print('\t');
            //dist_m = dist * 0.01;
            //Serial.print(dist*0.01); // distance in meter
            //Serial.print("METER");
            //Serial.print('\t');
            //Serial.print('\t');
            //Serial.print("strength = ");
            Serial.print(strength);// output signal strength value
            Serial.print('\n');
          }
        }
      }
    }
  }
}
