from imports import *
from motor_control.stepmotor_control import StepMotorController
from test_pantilt_class import *
from test_detect_class import *
print('imports set..')


class Robot:
    def __init__(self):

        self.human_detection = HumanDetection(
            model_path='/home/roboin/ResQ4U/RaspberryPi_src/all_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite', # file path would be changed
            labels_path='/home/roboin/ResQ4U/RaspberryPi_src/all_models/coco_labels.txt'
        )

        self.pan_tilt = PanTilt()
        print('init!')


    def run(self):
        if not self.human_detection.initialize():
            print('detection NOT initialized')
            return

        while True:
            ret, frame = self.human_detection.cap.read()
            if not ret:
                print('not ret')
                break
            if self.human_detection.if_detected(frame):
                print("!detected!")
                self.pan_tilt.frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
                self.pan_tilt.pan_tilt_to_match_frame_center_to_bounding_box_center()
                print("target in threshold")
            if not self.human_detection.if_detected(frame):
                print("not... detected...")
                self.pan_tilt.bounding_box_center = None
                print('motor not moving bc not detected')

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # cap.release()
        self.human_detection.not_detected()
        cv2.destroyAllWindows()

if __name__ =="__main__":
    ROBOT = Robot()
    ROBOT.run()
