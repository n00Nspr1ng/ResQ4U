SoftwareSerial TF02_Serial(LIDAR_RX, LIDAR_TX);

int dist;
int strength;
int check;
int loop_i;
int uart[9];

const int                     HEADER = 0x59;  // Data type

const int              FILTER_LENGTH = 10;    // Length of Moving Average
const int                   DIST_MIN = 100;   // 필터링할 최소 거리값
const int                   DIST_MAX = 4000;  // 필터링할 최대 거리값
const int         STRENGTH_THRESHOLD = 50;    // 필터링할 최대 신호 강도
const int         DISTANCE_THRESHOLD = 300;   // 이상치를 판단하기 위한 거리값의 임계값
const int            COUNT_THRESHOLD = 20;    // 이전의 평균 거리값을 유지할 카운트 임계값
const int   FINAL_DIST_BUFFER_LENGTH = 20;


int    filtered_dist[FILTER_LENGTH];
int    sum_dist = 0;
int    avg_dist = 0;
int         idx = 0;
int       count = 0;
bool  dist_flag = false;  // Align 되면 true
int      loop_j = 0;
int  final_dist = 0;

bool calculation_flag = false;

void initialize_lidar() {
  TF02_Serial.begin(115200);
  Serial.println("Done LiDAR initialization");
}


int calculate_final_dist() {  
  if (avg_dist > 0) {
    final_dist += avg_dist;
    loop_j += 1;
  }
  if (loop_j == FINAL_DIST_BUFFER_LENGTH) {
    final_dist /= FINAL_DIST_BUFFER_LENGTH;
    Serial.print("final_distance = ");
    Serial.print(final_dist);
    Serial.print('\n');
    calculation_flag = true;
    dist_flag = false;
    loop_j = 0;
  }
}


void filter() {
  if (strength >= STRENGTH_THRESHOLD && dist >= DIST_MIN && dist <= DIST_MAX) {
    count = 0;

    // 이동평균 필터
    sum_dist -= filtered_dist[idx];
    filtered_dist[idx] = dist;
    sum_dist += filtered_dist[idx];
    idx = (idx + 1) % FILTER_LENGTH;
    
    // 노이즈 및 이상치 제거
    int mean = sum_dist / FILTER_LENGTH;
    float variance = 0;
    for (int i = 0; i < FILTER_LENGTH; i++) {
      variance += pow(filtered_dist[i] - mean, 2);
    }
    variance /= FILTER_LENGTH;
    float std_dev = sqrt(variance);
    for (int i = 0; i < FILTER_LENGTH; i++) {
      if (abs(filtered_dist[i] - mean) > DISTANCE_THRESHOLD || abs(filtered_dist[i] - mean) > std_dev) {
        filtered_dist[i] = mean; // 이상치를 평균값으로 대체
      }
    }

    // 평균값 출력
    avg_dist = sum_dist / FILTER_LENGTH;

    if (dist_flag) {
      Serial.println("calculating");
      calculate_final_dist();
    }
  }
  else {
    count = count + 1;
    if (count >= COUNT_THRESHOLD) {
      avg_dist = 0;
    }
  }
}


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
    // Temporary (Enter 입력하면 dist_flag true)
//    if (Serial.available() > 0) {
//      if (Serial.read() == '\n') {
//        dist_flag = true;
//      }
//    }
  }
}


void put_dist_flag()
{
  dist_flag = true;
}


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
