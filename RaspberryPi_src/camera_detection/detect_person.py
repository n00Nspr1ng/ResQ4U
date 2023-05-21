# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo that runs object detection on camera frames using OpenCV.

TEST_DATA=../all_models

Run face detection model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels ${TEST_DATA}/coco_labels.txt

"""
import argparse
import cv2
import os

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

class personDetector():
    def __init__(self, show_image=True):
        self.show_image = show_image

        # Flag for detection start
        self.is_detected = False
        self.tracking = False
        self.count = 0

        # Initialize bounding box center point
        self.xc = 0
        self.yc = 0
        
        # Input image size
        self.height = 480
        self.width = 640
        
        self.crop_size = 300
        self.cropped_im_center = [0, 0]
        self.sliding_idx_x = 3
        self.sliding_idx_y = 2
        self.sliding_pixel_x = int((self.width - self.crop_size) / (self.sliding_idx_x - 1))
        self.sliding_pixel_y = int((self.height - self.crop_size) / (self.sliding_idx_y - 1))

        self.align_offset = 10
        
        self.i = 0
        self.j = 0

    def detect(self):
        default_model_dir = 'all_models'
        default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
        # default_model = 'yolov5s-int8-224_edgetpu.tflite'
        default_labels = 'coco_labels.txt'
        parser = argparse.ArgumentParser()
        parser.add_argument('--model', help='.tflite model path',
                            default=os.path.join(default_model_dir,default_model))
        parser.add_argument('--labels', help='label file path',
                            default=os.path.join(default_model_dir, default_labels))
        parser.add_argument('--top_k', type=int, default=3,
                            help='number of categories with highest score to display')
        parser.add_argument('--camera_idx', type=int, help='Index of which video source to use. ', default = 0)
        parser.add_argument('--threshold', type=float, default=0.5,
                            help='classifier score threshold')
        args = parser.parse_args()

        print('Loading {} with {} labels.'.format(args.model, args.labels))
        interpreter = make_interpreter(args.model)
        interpreter.allocate_tensors()
        labels = read_label_file(args.labels)
        inference_size = input_size(interpreter)

        # cap = cv2.VideoCapture(args.camera_idx)
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Visualize grid
            # cv2_im = cv2.line(frame, (int(self.width / 2), 0), (int(self.width / 2), self.height), (255,255,255), 1)
            # cv2_im = cv2.line(frame, (0, int(self.height / 2)), (self.width, int(self.height / 2)), (255,255,255), 1)
            # cv2_im = cv2.line(frame, (0, int(self.height / 2) + self.align_offset), (self.width, int(self.height / 2) + self.align_offset), (255,255,255), 1)

            if self.j < self.sliding_idx_y - 1:
                if self.i < self.sliding_idx_x - 1:
                    self.i += 1
                else:
                    self.i = 0
                    self.j += 1
            else:
                if self.i < self.sliding_idx_x - 1:
                    self.i += 1
                else:
                    self.i = 0
                    self.j = 0
            
            # Crop image
            if (self.tracking == True):
                self.cropped_im_center[0] = max(min(self.xc, self.width - int(self.crop_size / 2)), int(self.crop_size / 2))
                self.cropped_im_center[1] = max(min(self.yc, self.height - int(self.crop_size / 2)), int(self.crop_size / 2))
            else:
                self.cropped_im_center = [int(self.crop_size / 2 + self.sliding_pixel_x * self.i), int(self.crop_size / 2 + self.sliding_pixel_y * self.j)]
            y1 = self.cropped_im_center[1] - int(self.crop_size / 2)
            y2 = self.cropped_im_center[1] + int(self.crop_size / 2)
            x1 = self.cropped_im_center[0] - int(self.crop_size / 2)
            x2 = self.cropped_im_center[0] + int(self.crop_size / 2)
            cv2_im = frame[y1:y2, x1:x2]

            cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
            cv2_im_rgb = cv2.resize(cv2_im_rgb, inference_size)
            run_inference(interpreter, cv2_im_rgb.tobytes())
            objs = get_objects(interpreter, args.threshold)[:args.top_k]
            cv2_im = self.append_objs_to_img(cv2_im, inference_size, objs, labels)
            cv2_im = cv2.rectangle(cv2_im, (0, 0), (self.crop_size, self.crop_size), (0, 0, 255), 2)
            
            if self.show_image == True:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    def append_objs_to_img(self, cv2_im, inference_size, objs, labels):
        height, width, channels = cv2_im.shape
        scale_x, scale_y = width / inference_size[0], height / inference_size[1]
        self.is_detected = False
            
        for obj in objs:
                
            if labels[obj.id] == 'person':
                self.count = 0
                self.is_detected = True
                bbox = obj.bbox.scale(scale_x, scale_y)
                x0, y0 = int(bbox.xmin), int(bbox.ymin)
                x1, y1 = int(bbox.xmax), int(bbox.ymax)

                self.xc = self.cropped_im_center[0] - int(self.crop_size / 2) + int((x0+x1)/2)
                self.yc = self.cropped_im_center[1] - int(self.crop_size / 2) + int((y0+y1)/2)
                print(self.xc, self.yc)

                percent = int(100 * obj.score)

                label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))
                cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
                cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
                cv2_im = cv2.circle(cv2_im, (int((x0+x1)/2), int((y0+y1)/2)), 3, (255,255,255), -1)
        
        if (self.is_detected == True):
            self.count = 0
            self.tracking = True
        else:
            self.count += 1
            if (self.count > 20):
                self.tracking = False
                self.count = 0

        return cv2_im
        

    def get_center(self):
        return self.xc, self.yc


if __name__ == '__main__':
    detector = personDetector()
    detector.detect()
    print(detector.get_center())