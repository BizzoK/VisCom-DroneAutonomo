import cv2 as cv
img = cv.imread('aprendizado\Photos\park.jpg')

# Converting to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#cv.imshow('Gray', gray)

# Gaussian Blur
blur = cv.GaussianBlur(img, (5,5), cv.BORDER_DEFAULT)
#cv.imshow('Blur', blur)

# Average Blur
average = cv.blur(img, (7,7))

# Edge Cascade
canny = cv.Canny(blur, 175, 175)
#cv.imshow('Canny Edges', canny)

# Dilating the image
dilated = cv.dilate(canny, (7,7), iterations=3)
#cv.imshow('Dilated', dilated)

# Eroding
eroded = cv.erode(dilated, (7,7), iterations=3)
#cv.imshow('Eroted', eroded)

# Resize
resized = cv.resize(img, (500,500), interpolation=cv.INTER_LINEAR)
#cv.imshow('Resized', resized)

# Cropping
cropped = img[50:200, 200:400]
#cv.imshow('Cropped', cropped)

cv.waitKey(0)