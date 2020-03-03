import cv2
import numpy as np

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

cam = cv2.VideoCapture(0)

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))


while True:
    ret, frame = cam.read()

    middleOfRes = 240

    #convert BGR to HSV
    imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    #conts, h, = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    conts, _= cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(conts)):
                c =  max(conts,key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 5:
                    x,y,w,h=cv2.boundingRect(conts[i])
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255), 2)
                    xcenter = (int(M["m10"] / M["m00"]))
                    #print(xcenter)
                    if xcenter => 0:
                        xOffset1 = int(xcenter - middleOfRes)
                        xOffset = xOffset1
                    if xcenter < 0:
                        xOffset1 = int(xcenter - middleOfRes)
                        xOffset = xOffset1 * -1

                    print(xOffset)
                else:
                    break
    cv2.imshow("maskClose",maskClose)
    cv2.imshow("maskOpen",maskOpen)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",frame)
    cv2.waitKey(10)
