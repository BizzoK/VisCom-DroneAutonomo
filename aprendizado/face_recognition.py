import cv2 as cv
import numpy as np

haar_cascade = cv.CascadeClassifier('aprendizado\haar_face.xml')

people = ['Ben Affleck', 'Elton John', 'Jerry Seinfield','Madonna','Mindy Kaling']
#features = np.load('aprendizado\features.npy', allow_pickle=True)
#labels = np.load('aprendizado\labels.npy', allow_pickle=True)

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read(r'aprendizado\face_trained.yml')

img = cv.imread(r'C:\Projetos pessoais\VisCom DeltaV\aprendizado\Faces\val\elton_john\5.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

#cv.imshow('Recognition Test',gray)

# Detect the face in the image
faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 4)

for (x,y,w,h) in faces_rect:
    faces_roi = gray[y:y+h,x:x+w]

    label, confidence = face_recognizer.predict(faces_roi)
    print(f'Label = {people[label]} with a confidence of {confidence:.0f}%')

    cv.putText(img, str(people[label]), (20,20), cv.FONT_HERSHEY_COMPLEX, 
               1.0, (0,255,0), thickness=2)
    cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)

cv.imshow('Detected Face', img)
cv.waitKey(0)