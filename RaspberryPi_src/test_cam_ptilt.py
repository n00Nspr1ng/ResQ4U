from imports import *
from motor_control.stepmotor_control import StepMotorController
print('imports set..')

class HumanDetection:
    def __init__(self, model_path, label_path, top_k=3, threshold=0.1):
        self.model_path = model_path
        self.label_path = label_path
        self.top_k = top_k
        self.threshold = threshold
        self.labels = read_label_file(label_path)
        self.interpreter = make_interpreter(model_path)
        self.interpreter.allocate_tensors()
        self.inference_size = input_size(self.interpreter)

    def is_human_detected(self, cv2_im):
        cv2_im_rgb = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
        cv2_im_rgb = cv2.resize(cv2_im_rgb, self.inference_size)
        run_inference(self.interpreter, cv2_im_rgb.tobytes())
        objs = get_objects(self.interpreter, self.threshold)[:self.top_k]
        for obj in objs:
            if self.labels[obj.id] == 'person':
                bounding_box = obj.bbox
                bounding_box_center = (
                    int((bounding_box[0] + bounding_box[2]) / 2),
                    int((bounding_box[1] + bounding_box[3]) / 2)
                )
                return True, bounding_box_center
        return False, None
    
class PanTilt:
    def __init__(self):
        self.frame_center = None
        self.bounding_box_center = None
        
        self.panMotor = StepMotorController(config.pan_motor, gear_ratio=4)
        self.tiltMotor = StepMotorController(config.tilt_motor, gear_ratio=4)

        self.panMotor.return_to_initial()
        self.tiltMotor.return_to_initial()


    def pan_tilt_to_match_frame_center_to_bounding_box_center(self): # used previous algorithm I made..
        
        error_threshold =  1
        pan_step        = 15
        tilt_step       =  5

        error_x = self.frame_center[0] - self.bounding_box_center[0]
        error_y = self.frame_center[1] - self.bounding_box_center[1]

        if (abs(error_x) > error_threshold) or (abs(error_y) > error_threshold):
            if error_x > 0:
                self.pan_angle += pan_step
            else:
                self.pan_angle -= pan_step
            if error_y > 0:
                self.tilt_angle += tilt_step
            else:
                self.tilt_angle -= tilt_step

            self.pan_angle = max(50, min(130, self.pan_angle))
            self.tilt_angle = max(0, min(70, self.tilt_angle))

            self.panMotor.move(angle=self.pan_angle, ccw_dir=-1)
            self.tiltMotor.move(angle=self.tilt_angle, ccw_dir=-1)


class Robot:
    def __init__(self):
        self.human_detection = HumanDetection(
            model_path='../all_models/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite', # file path would be changed
            label_path='../all_models/coco_labels.txt'
        )
        self.pan_tilt = PanTilt()


    def run(self):
        threshold = 50  # set threshold value
        cap = cv2.VideoCapture('/dev/vidoe0', cv2.CAP_V4L)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if self.human_detection.is_human_detected(frame):
                print("!detected!")
                self.pan_tilt.frame_center = (frame.shape[1] // 2, frame.shape[0] // 2)
                self.pan_tilt.pan_tilt_to_match_frame_center_to_bounding_box_center()
                print("target in threshold")
            else:
                print("not... detected...")
                self.pan_tilt.bounding_box_center = None
                print('motor not moving bc not detected')

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()