SoftwareSerial TF02_Serial(LIDAR_RX, LIDAR_TX);

int dist;
int strength;
int check;
int loop_i;
int uart[9];

const int                     HEADER = 0x59;  // Data type

const int              FILTER_LENGTH = 10;    // Length of Moving Average
const int                   DIST_MIN = 100;   // Min distance to filter
const int                   DIST_MAX = 4000;  // Max distance to filter
const int         STRENGTH_THRESHOLD = 50;    // Strength threshold to fileter
const int         DISTANCE_THRESHOLD = 300;   // Distance threshold for ouliers
const int            COUNT_THRESHOLD = 20;    // Count threshold to hold mean distance
const int   FINAL_DIST_BUFFER_LENGTH = 20;

int    filtered_dist[FILTER_LENGTH];
int    sum_dist = 0;
int    avg_dist = 0;
int         idx = 0;
int       count = 0;
int      loop_j = 0;
int  final_dist = 0;

bool       align_flag = false; 
bool calculation_flag = false;


void initialize_lidar() {
  TF02_Serial.begin(115200);
  Serial.println("Done LiDAR initialization");
}

/*
Function for lidar loop
- receive data from lidar then filter
- prints "filtering" every time lidar receives data (Note that Lidar doesn't returns value every loop)
*/
void lidar_loop() {
  if (TF02_Serial.available()) {
    if (TF02_Serial.read() == HEADER) {
      uart[0] = HEADER;
      if (TF02_Serial.read() == HEADER) {
        uart[1] = HEADER;
        for (loop_i = 2; loop_i < 9; loop_i++) {
          uart[loop_i] = TF02_Serial.read();
        }
        check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];
        if (uart[8] == (check & 0xff)) {
          dist = uart[2] + uart[3] * 256;
          strength = uart[4] + uart[5] * 256;
          Serial.println("filtering");
          filter();
        }
      }
    }
  }
}

/*
Function for filtering
- uses moving average filter to get the distance
- prints "calculating" & calculate_final_dist() runs after aling_flag==True
*/
void filter() {
  if (strength >= STRENGTH_THRESHOLD && dist >= DIST_MIN && dist <= DIST_MAX) { //when detected
    count = 0;

    // Moving Average Filter
    sum_dist -= filtered_dist[idx];
    filtered_dist[idx] = dist;
    sum_dist += filtered_dist[idx];
    idx = (idx + 1) % FILTER_LENGTH;
    
    // Filter noise & outliers
    int mean = sum_dist / FILTER_LENGTH;
    float variance = 0;
    for (int i = 0; i < FILTER_LENGTH; i++) {
      variance += pow(filtered_dist[i] - mean, 2);
    }
    variance /= FILTER_LENGTH;
    float std_dev = sqrt(variance);
    for (int i = 0; i < FILTER_LENGTH; i++) {
      if (abs(filtered_dist[i] - mean) > DISTANCE_THRESHOLD || abs(filtered_dist[i] - mean) > std_dev) {
        filtered_dist[i] = mean; // swap outiler with mean value
      }
    }

    // Average distance
    avg_dist = sum_dist / FILTER_LENGTH;
    
    // Calculate final distance when aligned
    if (align_flag) {
      Serial.println("calculating");
      calculate_final_dist();
    }
  }
  else { //when not detected
    count = count + 1;
    if (count >= COUNT_THRESHOLD) {
      avg_dist = 0;
    }
  }
}

/*
Function for calculating final distance after align flag
*/
int calculate_final_dist() {  
  if (avg_dist > 0) {
    final_dist += avg_dist;
    loop_j += 1;
  }
  
  // At final calculating loop
  if (loop_j == FINAL_DIST_BUFFER_LENGTH) { 
    final_dist /= FINAL_DIST_BUFFER_LENGTH;
    Serial.print("final_distance = ");
    Serial.print(final_dist);
    Serial.print('\n');
    calculation_flag = true;
    align_flag = false;
    loop_j = 0;
  }
}

/*
Function to assign align_flag
*/
void put_align_flag()
{
  align_flag = true;
}

/*
Function to return final distance
- returns 0 when calculating is not done.
- returns dist when calculating is done.
*/
int get_final_dist()
{
  if (calculation_flag == false)
  {
    return 0;
  }
  else if (calculation_flag == true)
  {
    calculation_flag = false;
    return final_dist;
  }
}
