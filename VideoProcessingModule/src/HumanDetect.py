# import the necessary packages
import numpy as np
import cv2
import time
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()
fname = "./croppedimg/human/"
# open webcam video stream
cap = cv2.VideoCapture(0)
i = 0
def draw_left_path(img,x,y,w,h):
    start_point = x+w
    cv2.line(img, (320-2*w,480), (start_point, y+int(h)), (255,0,0), 8) #4픽셀 선 그리기
    cv2.line(img, (start_point, y+int(h)), (start_point+int(w/5),y+int(h-20)), (255, 0, 0), 10)
    start_point = x+2*w
    cv2.line(img, (540,480), (start_point, y+int(h)), (255,0,0), 8) #4픽셀 선 그리기
   # cv2.line(img, (start_point, y+int(h)), (start_point+int(w/5),y+int(h-20)), (255, 0, 0), 10)
    return img
def draw_right_path(img, x, y, w, h):
    start_point = x
    cv2.line(img, (320+2*w, 480), (start_point, y+int(h)), (255, 0, 0), 8)  # 8픽셀 선 그리기
    cv2.line(img, (start_point, y+int(h)), (start_point - int(w/5), y+int(h-20)), (255, 0, 0), 8)
    start_point = x-2*w
    cv2.line(img, (100, 480), (start_point, y + int(h)), (255, 0, 0), 8)  # 8픽셀 선 그리기
   # cv2.line(img, (start_point, y + int(h)), (start_point - int(w / 5), y + int(h-20)), (255, 0, 0), 8)
    return img
while (True):
    # Capture frame-by-frame
    start = time.time()
    ret, frame = cap.read()
    # resizing for faster detection[240,160] [320 * 240]
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8, 8))
    detectCount = 0
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                      (0, 255, 0), 2)
        cv2.putText(frame, "Detect", (xA - 50, yA - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
        detectCount = detectCount+1
        if(detectCount>1):
            print("Waiting...")
        else :
            if(i%10 == 0):
                cropped = frame[yA:yB,xA:xB]
                #print("xA : {0}, xB : {1}, yA : {2}, yB : {3}".format(xA, xB,yA,yB))  # Print Width, Height of Cropped Area
                i=0
            if(xB < 380 and xA<260):
                print("Left Side Detect.")
                try:
                    frame = draw_left_path(frame, xA,yA,xB-xA,yB-yA)
                except:
                    pass
            elif(xA>260 and xB>380):
                print("Right Side Detect")
                try:
                    frame = draw_right_path(frame, xA, yA, xB - xA, yB - yA)
                except:
                    pass
            else:
                try:
                    frame = draw_right_path(frame, xA, yA, xB - xA, yB - yA)
                except:
                    pass
                print("Center Side Detect")
        s = fname + str(i)+'.jpg'
        cv2.imwrite(s, cropped) # IMG File Write
        print("time :", time.time() - start)
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