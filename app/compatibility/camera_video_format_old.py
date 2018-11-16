from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys

## Raspeberry Pi tests

def capture_camera():
    # initialize the camera and grab a reference to the raw camera capture
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32
    rawCapture = PiRGBArray(cam, size=(640, 480))

    time.sleep(0.1)


    # We acknowledge capturing a 30 fps video
    while True:
        #récupération de l'image fournie par la caméra
        #puis conversion en array numpy
        raw_capture = PiRGBArray(cam, size=(640, 480))
        cam.capture(raw_capture, format="bgr")
        frame = raw_capture.array

        out_frame = frame.copy()
        cv2.putText(out_frame, "Raspberry camera test", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        #affichage de l'image
        cv2.imshow("Face detection using TensorFlow", out_frame)

        # interval to let the system process imshow
        key = cv2.waitKey(10)



capture_camera()
