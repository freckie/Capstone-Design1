# import the necessary packages
import numpy as np
import cv2
import time
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()
fname = "./croppedimg/"
# open webcam video stream
cap = cv2.VideoCapture(0)
i = 0
while (True):
    # Capture frame-by-frame
    start = time.time()
    ret, frame = cap.read()
    # resizing for faster detection[240,160] [320 * 240]
    frame = cv2.resize(frame, (240, 160))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                      (0, 255, 0), 2)
        if(i%10 == 0):
            cropped = frame[yA:yB,xA:xB]
            s = fname + str(i)+'.jpg'
            cv2.imwrite(s, cropped) # IMG File Write
            print("time :", time.time() - start)
            print("Human Detect!") #Alert
            if(i > 200):
                i=0
        i= i+1
    # Display the resulting frame


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
# and release the output
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)