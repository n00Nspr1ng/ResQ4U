#include<SoftwareSerial.h>// soft serial port header file
SoftwareSerial Serial1(2,3); // define the soft serial port as Serial1, pin2 as RX, and pin3 as TX
/*For Arduino board with multiple serial ports such as DUE board, comment out the above two codes, anddirectlyuseSerial1 port*/
int dist;// LiDAR actually measured distance value
int strength;// LiDAR signal strength
int check;// check numerical value storage
int i;
int uart[9];// store data measured by LiDAR
const int HEADER=0x59;// data package frame header
void setup()
{
  Serial.begin(9600);//set the Baud rate of Arduino and computer serial port
  Serial1.begin(115200);//set the Baud rate of LiDAR and Arduino serial port
}
