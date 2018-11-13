import numpy as np
import cv2

def display(file):
    """Prints image and wait for the user to press any key"""
    img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
    cv2.imshow('Image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def blur(file):
    """Returns the grayscale edges of the image detected with Canny Edge Detection"""
    img = cv2.imread(file,cv2.IMREAD_GRAYSCALE)
    return cv2.Canny(img,100,200)