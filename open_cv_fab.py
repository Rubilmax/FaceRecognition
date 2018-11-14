import numpy as np
import cv2

def load_and_display_image(file_name):
    image=cv2.imread(file_name)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



