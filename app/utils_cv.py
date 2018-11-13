import numpy as np
import cv2

def display(file):
    img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
    cv2.imshow('Image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
