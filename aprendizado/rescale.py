import cv2 as cv

#img = cv.imread('aprendizado\Photos\cat.jpg')
#cv.imshow('cat', img)

def rescaleFrame(frame, scale=0.75):
    #Images, Videos and Live Video
    width = int(frame.shape[1] * scale) 
    heigth = int(frame.shape[0] * scale )
    dimensions = (width, heigth)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

resized_image = rescaleFrame(img)
cv.imshow('Image', resized_image)

def changeRes(width, heigth):
    # Live Video Only
    capture.set(3,width)
    capture.set(4,heigth)


#Reading Videos
capture = cv.VideoCapture('aprendizado\Videos\dog.mp4')

while True:
    isTrue, frame = capture.read()

    frame_resized = rescaleFrame(frame)

    cv.imshow('Video', frame)
    cv.imshow("Video Resized", frame_resized)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

capture.release()
cv.destroyAllWindows()