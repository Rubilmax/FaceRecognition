import numpy as np
import cv2

def display(file):
    """Prints image and wait for the user to press any key"""
    img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
    cv2.imshow('Image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def blob(file, size):
    img = cv2.imread(file,cv2.IMREAD_UNCHANGED)
    cv2.imshow('Image',cv2.dnn.blobFromImage(img, 1.0, size, [104, 117, 123], False, False))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def blur(file):
    """Returns the grayscale edges of the image detected with Canny Edge Detection"""
    img = cv2.imread(file,cv2.IMREAD_GRAYSCALE)
    return cv2.Canny(img,100,200)

def bw(file_name):
    """Returns the black and white image corresponding to the image"""
    image = cv2.imread(file_name,0)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()