import cv2 as cv
import numpy as np

img = cv.imread('aprendizado\Photos\cats.jpg')
blank = np.zeros(img.shape, dtype='uint8')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
""" blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny', canny)
 """

# Threshold tries to binarize the image
ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
cv.imshow('Thresh', thresh)

contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} countours found!')

cv.drawContours(blank, contours, -1, (255,0,255), 1)
cv.imshow('Contours Drawn', blank)




cv.waitKey(0)