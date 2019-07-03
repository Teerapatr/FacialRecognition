from tkinter import *
from PIL import Image, ImageTk
def detaset():
    import cv2
    import os

    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    font = cv2.FONT_HERSHEY_SIMPLEX

    # For each person, enter one numeric face id
    face_id = input('\n enter user id end press <return> ==>  ')

    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    while(True):

        ret, img = cam.read()
        img = cv2.flip(img, 1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)   
            count += 1

            # Save the captured image into the datasets folder
            cv2.putText(img, str(count), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('image', img)

        

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30: # Take 30 face sample and stop video
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
def detaset2():
    import cv2
    import numpy as np
    from PIL import Image
    import os

    # Path for face image database
    path = 'dataset'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

    # function to get the images and label data
    def getImagesAndLabels(path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids

    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
def detaset3():
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

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Aum', 'June', 'Pe', 'Jame', 'Pichet', 'Phon', 'Att', 'Neung'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

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

    while True:

        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

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
            if (confidence < 80):
                id = names[id]
                confidence = "  {0}%".format(round(80 - confidence))
                #GPIO.output(27,1)
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(80 - confidence))
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
                    
                if (lock2[id]):
                    GPIO.output(27,1)
                   
            
                
                
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
            
            
                
                 
        cv2.imshow('camera',img)

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    GPIO.output(27,0)
    cam.release()
    cv2.destroyAllWindows()
gui=Tk()
gui.geometry("480x480")
gui.title("Face Recognition CET")
gui.configure(background='#EECFA1')
mlabel=Label(text="Face Recognition",font='times 18',fg="blue", bg='#EECFA1').pack()

img = Image.open("Rmutr.png")
photo = ImageTk.PhotoImage(img)
lbl = Label(image=photo, bg='#EECFA1').place(x=190,y=40)

mButton=Button(text="Dataset",command=detaset).place(x=40,y=280)
mButton2=Button(text="Train",command=detaset2).place(x=40,y=320)
mButton3=Button(text="Recognition",command=detaset3).place(x=40,y=360)
mEntry = Entry(width=10).place(x=140,y=285)
mEntry2 = Entry(width=10).place(x=240,y=285)
mButton4=Button(text="Ok",command=detaset3).place(x=350,y=280)
gui.mainloop()