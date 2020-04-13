import cv2
import numpy as np
import time
fname = "./croppedimg/"
def bboxes(inp):
    #Frame을 인자로 전달받음
    img = inp
    start = time.time()
    index = 0
    # img2gray = cv2.imread(fname,0)
    # img = cv2.namedWindow(img,cv2.WINDOW_NORMAL)
    # img = cv2.resizeWindow(img,600,600)
    img_final = inp
    # img_final = cv2.namedWindow(fname,cv2.WINDOW_NORMAL)
    # img_final = cv2.resizeWindow(fname,600,600)
    img2gray = cv2.cvtColor(inp, cv2.COLOR_BGR2GRAY) #GRAY Image 8bit per pixel
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY) #threshold : distinguish background, object
    image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask) #bitwise
    ret, new_img = cv2.threshold(img_final, 180, 255, cv2.THRESH_BINARY)  # Nfor black text , cv.THRESH_BINARY_IV
    newimg = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY) #Gray Image converting

    # remove noise from image
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,1))
    # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
    dilated = cv2.dilate(newimg, kernel, iterations=3)  # dilate
    _, contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours
    #cv2.CHAIN_APPROX_NONE: 모든 컨투어 포인트를 반환
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # remove small false positives that aren't text
        # text인식하기. width, height
        if w < 80 and h < 80:
            continue
        if h / w > 9.0 or w / h > 9.0:
            continue

        # draw rectangle around contour on original image
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        # 이미지 주변 시작좌표를 기준으로 사각형틀그리기
        cropped = img_final[y :y +  h , x : x + w]
        s = fname +"Text"+ str(index) + '.jpg'
        cv2.imwrite(s, cropped)
        if(index % 10 == 0 ):
            cv2.imwrite(s, cropped)
            print("[Processing time ]:", time.time() - start)
            if(index>20):
                index=0
        index = index + 1

    # write original image with added contours to disk
    imgres = cv2.resize(img, (320, 240))
    cv2.imshow('captcha_result', imgres)


cap = cv2.VideoCapture(0) #동영상 파일 읽어옴
while (cap.isOpened()):
    ret, inp = cap.read() #프레임을 읽어옴, 읽어온 프레임을 인자로 bboxes 전달
    if(ret): #success boolean
        bboxes(inp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Terminate Process..")
        break
cap.release() #파일 닫아줌