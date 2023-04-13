import av
import cv2
import logging

logging.basicConfig(level=logging.INFO)

RTSP_URL = "rtsp://192.168.0.1"
#RTSP_URL = "rtsp://<username>:<password>@<ip>/axis-media/media.amp"

def rtsp_to_opencv(url):
    logging.info(f' Try to connect to {url}')
    # Connect to RTSP URL
    video = av.open(url, 'r')
    try:
        # Iter over Package to get an frame
        for packet in video.demux():
            # When frame is decoded
            for frame in packet.decode():
                # Convert frame to ndarray for opencv
                img = frame.to_ndarray(format='bgr24')
                # Show Frame
                cv2.imshow("Rtsp to opencv", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        pass
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        rtsp_to_opencv(RTSP_URL)
    except Exception as error:
        logging.error(error)
