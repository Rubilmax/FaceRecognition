# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)


## Raspeberry Pi tests

def camera(seconds):
    frame_count = 0
    # We acknowledge capturing a 30 fps video
    while frame_count < seconds * 30:
        camera.capture(raw_capture, format="bgr")
        frame = raw_capture.array

        if not has_frame:
            break
        frame_count += 1

        out_frame = frame.copy()
        cv2.putText(out_frame, "Raspberry camera test", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        cv2.imshow("Face detection using TensorFlow", out_frame)

        # interval to let the system process imshow
        cv2.waitKey(10)
        # As we don't have any keyboard, we break after having showed 50 frames
    cv2.destroyAllWindows()
    # vid_writer.release()
