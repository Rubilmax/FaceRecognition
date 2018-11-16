#import utils_cv as utils
import face_recognition
#import deep_learner as dl
import cv2
import time
import sys
import imutils

#import os.path #to test file paths

## utils_cv tests

#utils.bw('..\\Data\\tetris_blocks.png')

## Raspeberry Pi tests

def camera(seconds):
    source = 0
    #By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    cap = cv2.VideoCapture(source)

    frame_count = 0
    #We acknowledge capturing a 30 fps video
    while frame_count < seconds*30:
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        out_frame = frame.copy()
        cv2.putText(out_frame, "Raspberry camera test", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        cv2.imshow("Face detection using TensorFlow", out_frame)

        #interval to let the system process imshow
        cv2.waitKey(10)
        #As we don't have any keyboard, we break after having showed 50 frames
    cv2.destroyAllWindows()
    #vid_writer.release()

#camera(5)

#utils.blob("..\\Data\\database\\train\\Romain\\test.png", (1000,1333))

#dl.process("..\\Data\\database\\test\\remi_1.jpg")