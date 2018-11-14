import numpy as np
import cv2

def load_and_display_image(file_name):
    image=cv2.imread(file_name) #Opens the file
    cv2.imshow('image',image)   #Displays the file
    cv2.waitKey(0)              #Waits for the user to press a key
    cv2.destroyAllWindows()     #Close the other windows

def load_and_display_bw(file_name): #Does the same but displays the image in black and white
    image=cv2.imread(file_name,0)
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



