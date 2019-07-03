from picamera import PiCamera
import numpy as np
import cv2
camera = PiCamera()
camera.resolution = (640, 480)
#rawCapture = PiRGBArray(camera, size=(640, 480))
while(True):
    ret, frame = camera.read()
    frame = cv2.flip(frame, -1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('frame', frame)
    cv2.imshow('gray', gray)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()