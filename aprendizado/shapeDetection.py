import cv2 as cv
img = cv.imread('aprendizado\shapes.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, thresh = cv.threshold(gray, 220, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
for i, contour in enumerate(contours):
    if i == 0: # Ignore the first contour (the whole image)
        continue

    # Approximate the shape we want
    epsilon = 0.01*cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    
    cv.drawContours(img, contour, 0, (255,255,0), 3)
    # Coordinates of the contour
    x,y,w,h = cv.boundingRect(approx)
    x_mid = int(x+20)
    y_mid = int(y-20)

    coords = (x_mid, y_mid)
    colour = (255,0,0)
    font = cv.FONT_HERSHEY_DUPLEX

    # Recognize the shape based on amount of corners
    if len(approx) == 3:
        cv.putText(img, "Triangle", coords, font, 1, colour, 1)
    elif len(approx) == 4:
        cv.putText(img, "Quadrilateral", coords, font, 1, colour, 1)
    elif len(approx) == 5:
        cv.putText(img, "Pentagon", coords, font, 1, colour, 1)
    elif len(approx) == 6:
        cv.putText(img, "Hexagon", coords, font, 1, colour, 1)
    else:
        cv.putText(img, "Circle", coords, font, 1, colour, 1)

cv.imshow('Shapes', img)
cv.waitKey(0)