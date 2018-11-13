pip install picamera

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(10)
camera.stop_preview()

## faire une rotation de 180°

'''camera.rotation = 180
camera.start_preview()
sleep(10)
camera.stop_preview()'''

## Changer la transparence

'''from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview(alpha=200)
sleep(10)
camera.stop_preview()'''

## prendre une photo
'''camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/image.jpg')
camera.stop_preview()'''

## 5 Photos d'affilée
'''camera.start_preview()
for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()'''
