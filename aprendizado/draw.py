import cv2 as cv
import numpy as np

blank = np.zeros((500,500,3), dtype='uint8') #dataType image

# 1. Paint the image a certain colour
#blank[200:300, 300:400] = 0,0,255 #Turning all pixels green
#cv.imshow('Green', blank)

# 2. Draw a Rectangle
cv.rectangle(blank, (0,100), (250,500), (0,255,0), thickness=-1)
#cv.imshow('Rectangle', blank)

# 3. Draw a Circle
cv.circle(blank, (250,250), 80, (0,0,255), thickness=3)
#cv.imshow('Circle', blank)

# 4. Draw a Line
cv.line(blank, (200,0), (250,250), (255,255,0), thickness=3)
#cv.imshow('Line', blank)

# 5. Write text
cv.putText(blank, 'Testando o texto', (0,255), cv.FONT_HERSHEY_TRIPLEX, 1.0, (100,150,0), 2)
cv.imshow('Text', blank)

cv.waitKey(0)