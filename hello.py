from picamera import PiCamera
from time import sleep

print('hello world')
camera = PiCamera()
sleep(2)
camera.capture('/home/pi/Desktop/cap.jpg')
