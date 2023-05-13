#include <SoftwareSerial.h>

SoftwareSerial Serial1(2,3);

int dist;
int strength;
int check;
int i;
int uart[9];

const int HEADER = 0x59;

const int FILTER_LENGTH = 10; // 이동평균 필터 길이
const int DIST_MIN = 100; // 필터링할 최소 거리값
const int DIST_MAX = 4000; // 필터링할 최대 거리값
const int STRENGTH_THRESHOLD = 50; // 필터링할 최대 신호 강도
const int DISTANCE_THRESHOLD = 300; // 이상치를 판단하기 위한 거리값의 임계값
const int COUNT_THRESHOLD = 20; // 이전의 평균 거리값을 유지할 카운트 임계값
const int FINAL_DIST_BUFFER_LENGTH = 20;

int filtered_dist[FILTER_LENGTH];
int sum_dist = 0;
int avg_dist = 0;
int idx = 0;
int count = 0;
bool dist_flag = false; // Align 되면 true
int j = 0;
int final_dist = 0;
bool launch_flag = false; // final_dist 계산 되면 true

void setup() {
  Serial.begin(9600);
  Serial1.begin(115200);
}

void get_final_dist() {
  if (avg_dist > 0) {
    final_dist += avg_dist;
    j += 1;
  }
  if (j == FINAL_DIST_BUFFER_LENGTH) {
    final_dist /= FINAL_DIST_BUFFER_LENGTH;
    Serial.print("final_distance = ");
    Serial.print(final_dist);
    Serial.print('\n');
    dist_flag = false;
    j = 0;
    final_dist = 0;
    launch_flag = true;
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
      get_final_dist();
    }
  }
  else {
    count = count + 1;
    if (count >= COUNT_THRESHOLD) {
      avg_dist = 0;
    }
  }
}

void loop() {
  if (Serial1.available()) {
    if (Serial1.read() == HEADER) {
      uart[0] = HEADER;
      if (Serial1.read() == HEADER) {
        uart[1] = HEADER;
        for (i = 2; i < 9; i++) {
          uart[i] = Serial1.read();
        }
        check = uart[0] + uart[1] + uart[2] + uart[3] + uart[4] + uart[5] + uart[6] + uart[7];
        if (uart[8] == (check & 0xff)) {
          dist = uart[2] + uart[3] * 256;
          strength = uart[4] + uart[5] * 256;
          
          filter();
        }
      }
    }
    // Temporary (Enter 입력하면 dist_flag true)
    if (Serial.available() > 0) {
      if (Serial.read() == '\n') {
        dist_flag = true;
      }
    }
  }
}
