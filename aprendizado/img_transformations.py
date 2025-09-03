import cv2 as cv
import numpy as np

img = cv.imread('aprendizado\Photos\park.jpg')
#cv.imshow('City', img)

# Translation
def translate(img, x, y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0]) # Width and height
    return cv.warpAffine(img, transMat, dimensions)
# -x --> Left
# -y --> Up
# x --> Right
# y --> Down
translated = translate(img, 100, 100) # Right and down
#cv.imshow('Translated', translated)

# Rotation
def rotate(img, angle, rotPoint=None):
    (height,width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2,height//2)

    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, 90) # For clockwise, negative angles
#cv.imshow('Rotated', rotated)

# Resizing
resized = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)
#cv.imshow('Resized', resized)

# Flipping
flip = cv.flip(img, -1) # 0=vertical, 1=horizontal,-1=both
#cv.imshow('Flipped', flip)

cv.waitKey(0)