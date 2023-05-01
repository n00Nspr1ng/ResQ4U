#include<SoftwareSerial.h>// soft serial port header file
SoftwareSerial TF02_Serial(2,3); // define soft serial port as TF02_Serial, pin2 as RX, and pin3 as TX

// (MEMO) PINS TO CONNECT
// 2->GREEN(RX)    3->WHITE(TX)
 
// Include the filters library @ https://github.com/JonHub/Filters
#include <Filters.h>

// Define the sampling frequency
#define SAMPLING_FREQUENCY 1000
// Define the cutoff frequency
#define CUTOFF_FREQUENCY_HP 30
#define CUTOFF_FREQUENCY_LP 6

// Create a high-pass filter object
FilterOnePole filter_HP = FilterOnePole(HIGHPASS, CUTOFF_FREQUENCY_HP);
// Create a low-pass filter object
FilterOnePole filter_LP = FilterOnePole(LOWPASS, CUTOFF_FREQUENCY_LP);

float LP_filtered_strength;
float HP_filtered_strength;


// create low-pass filter object
unsigned long previous_time = 0;
// previous time in milliseconds
const unsigned long sampling_period = 1000 / SAMPLING_FREQUENCY; // sampling period in milliseconds


int dist;// LiDAR actually measured distance value
int strength;// LiDAR signal strength
int check;// check numerical value storage
int i;
int uart[9];// store data measured by LiDAR
const int HEADER=0x59;// data package frame header

void setup()
{
  Serial.begin(9600);//set the Baud rate of Arduino and computer serial port
  TF02_Serial.begin(115200);//set the Baud rate of LiDAR and Arduino serial port
}

void loop()
{
  unsigned long current_time = millis(); // get current time in milliseconds
  if (current_time - previous_time >= sampling_period) {
    if (TF02_Serial.available())//check whether the serial port has data input
    {
      if(TF02_Serial.read()==HEADER)// determine data package frame header 0x59
      {
        uart[0]=HEADER;
        if(TF02_Serial.read()==HEADER)//determine data package frame header 0x59
        {
          uart[1]=HEADER;
          for(i=2;i<9;i++)// store data to array
          {
            uart[i]=TF02_Serial.read();
          }
          check=uart[0]+uart[1]+uart[2]+uart[3]+uart[4]+uart[5]+uart[6]+uart[7];
          if(uart[8]==(check&0xff))// check the received data as per protocols
          {
            dist=uart[2]+uart[3]*256;// calculate distance value
            // Apply the high-pass filter to distance value
            // float filtered_dist = filter.step(dist);  -- distance filter needed?

            // calculate signal strength value
            strength=uart[4]+uart[5]*256;

            /****** HIGH PASS ******/
            filter_HP.input(strength);
            // input raw strength value to filter
            HP_filtered_strength = filter_HP.output();

            /****** LOW PASS ******/
            filter_LP.input(strength);
            // input raw strength value to filter
            LP_filtered_strength = filter_LP.output();
            // Serial.print(LP_filtered_strength);/
            Serial.print(15000);
            Serial.print('\t');
            Serial.print(0);
            Serial.print('\t');
            Serial.print(strength);
            Serial.print('\t');
            // Serial.print(HP_filtered_strength);
            // Serial.print('\t');   
            Serial.println(LP_filtered_strength);
            // Serial.print('\t');/

            /****** SERIAL PRINT ******/
            // Serial.print("dist = ");
            // Serial.print(dist);// /output LiDAR tests distance value/
            // Serial.print('\t');
            // Serial.print("strength = ");
            // Serial.print(strength);// output signal strength value
            // Serial.print('\n');/

            /****** SERIAL PLOTTER ******/
            // Serial.println("filtered_DISTANCE filtered_STRENGTH_HP filtered_STRENGTH_LP");
            // Serial.println(HP_filtered_strength);
            // Serial.println(LP_filtered_strength);

            previous_time = current_time; // update previous time
          }
        }
      }
    }
  }
}
