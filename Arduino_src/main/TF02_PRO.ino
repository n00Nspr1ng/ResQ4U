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
const int DISTANCE_THRESHOLD = 300;
const int COUNT_THRESHOLD = 20; // 이전의 평균 거리값을 유지할 timestep

int filtered_dist[FILTER_LENGTH];
int sum_dist = 0;
int avg_dist = 0;
int idx = 0;
int count = 0;

void setup() {
  Serial.begin(9600);
  Serial1.begin(115200);
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
            
            // 평균값 출력
            avg_dist = sum_dist / FILTER_LENGTH;
        }
          }
          else {
            count = count + 1;
            if (count >= COUNT_THRESHOLD) {
              avg_dist = 0;
            }
          }

          // Printing
          // Serial.print("distance = ");
          // Serial.print(dist);
          // Serial.print('\t');
          // Serial.print('\t');
          // Serial.print("strength = ");
          // Serial.print(strength);
          // Serial.print('\t');
          // Serial.print('\t');
          // Serial.print("filtered_distance = ");
          // Serial.print(avg_dist);
          // Serial.print('\t');
          // Serial.print('\t');
          // Serial.print("count = ");
          // Serial.print(count);
          // Serial.print('\n');

          // Logging
          Serial.print(dist);
          Serial.print('\t');
          Serial.print(strength);
          Serial.print('\t');
          Serial.print(avg_dist);
          Serial.print('\t');
          Serial.print(count);
          Serial.print('\n');

          // Plotting
          // Serial.print(0);
          // Serial.print(",");
          // Serial.print(4000);
          // Serial.print(",");
          // Serial.print(avg_dist);
          // Serial.print(",");
          // Serial.println(dist);
        }
      }
    }
  }
}
