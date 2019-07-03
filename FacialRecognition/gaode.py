#!/usr/bin/env python3
import cv2
import numpy as np
import os
import RPi.GPIO as GPIO 

from datetime import datetime
import time
from firebase import firebase
firebase = firebase.FirebaseApplication('https://face-counter-2d3b8.firebaseio.com/')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)

font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Aum', 'June', 'Pe', 'Jame', 'Pichet', 'Phon', 'Att', 'Neung'] 

    # Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 320) # set video widht
cam.set(4, 240) # set video height
#cam.framerate(32)


    # Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

count = dict()
sec = dict()
lock = dict()
lock2 = dict()
data = dict()
count["Aum"] = 0
count["June"] = 0
count["Pe"] = 0
count["Jame"] = 0
count["Pichet"] = 0
count["Phon"] = 0
count["Att"] = 0
count["Neung"] = 0
count["unknown"] = 0
sec["Aum"] = 0
sec["June"] = 0
sec["Pe"] = 0
sec["Jame"] = 0
sec["Pichet"] = 0
sec["Phon"] = 0
sec["Att"] = 0
sec["Neung"] = 0
sec["unknown"] = 0
lock["Aum"] = True
lock["June"] = True
lock["Pe"] = True
lock["Jame"] = True
lock["Pichet"] = True
lock["Phon"] = True
lock["Att"] = True
lock["Neung"] = True
lock["unknown"] = True

lock2["Aum"] = 1
lock2["June"] = 1
lock2["Pe"] = 1
lock2["Jame"] = 1
lock2["Pichet"] = 1
lock2["Phon"] = 1
lock2["Att"] = 1
lock2["Neung"] = 1
lock2["unknown"] = 1

led_lock = True
led_sec = 0
lock_delay = True

while True:
        
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.IN)
        
    if (GPIO.input(22)):
        a = GPIO.input(22)
        a = 1
        GPIO.output(17,0)
        if((int(time.time()%100)-led_sec) > 5):
            led_lock = True
            GPIO.output(27,0)
            GPIO.output(19,0)
            
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        #cam.release()
        cv2.destroyAllWindows()
        lock_delay = True
    
    else:
        a = 0
        GPIO.output(17,1)
        
        
    
        if(lock_delay):
#            time.sleep(3)
            i = 0
            while(i < 10):
                ret, img =cam.read()
                ret, img =cam.read()
                ret, img =cam.read()
                i = i+1
            lock_delay = False
        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(gray)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
            )
            
            # secB = int(time.time()%1000)

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                

                # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 60):
                id = names[id]
                confidence = "  {0}%".format(round(60 - confidence))
                #GPIO.output(27,1)
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(60 - confidence))
                #GPIO.output(27,0) 
                
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)

            if(lock[id]):
                sec[id] = int(time.time()%1000)
                led_sec = int(time.time()%100)
                count[id] += 1
                print(id,count[id])
                lock[id] = False
                led_lock = False
                    
                if (lock2[id]):
                    lock2[id] = 1
                    lock2["unknown"] = 0
                    GPIO.output(27,0)
                    GPIO.output(19,0)
                        
                if (lock2[id]):
                    GPIO.output(27,1)
                    GPIO.output(19,1)
                       
                
                    
                    
                dt = time.strftime("%A %d %B %Y, %H:%M:%S")
                print (dt)
                data['count'] = count[id]
                data['datetime'] = dt
                firebase.post('/'+id,dt)

            if((int(time.time()%1000)-sec[id]) > 8):
                lock[id] = True
                    
        if(~led_lock):
                #print (led_lock)
            if((int(time.time()%100)-led_sec) > 5):
                led_lock = True
                GPIO.output(27,0)
                GPIO.output(19,0)
                
                
                    
                    
        cv2.imshow('camera',img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

GPIO.output(17,0)
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

