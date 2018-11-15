import cv2
import imutils

def capture():
    cap = cv2.VideoCapture(0)
    has, frame = cap.read()
    if has:
        cv2.imshow("test", frame)
        key = cv2.waitKey(0)
        while key != 27:
            key = cv2.waitKey(0)
        cv2.destroyAllWindows()

#capture()