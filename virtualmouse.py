import cv2
import numpy as np
import handtrackingmodule as htm
import time
import autopy

wCAM = 640
hCAM = 480


wSCRN, hSCRN = autopy.screen.size()
frameR  = 100

smoothen =5
plocX, plocY = 0,0
clocX, clocY = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wCAM)
cap.set(4,hCAM)
detector = htm.handDetector(max_hands=1)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    
    cv2.rectangle((img), (frameR, frameR), (wCAM - frameR, hCAM-frameR), (255,255,255),1)
    
    
    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
    
        fingers = detector.fingersUp()

    

        if fingers[1] == 1and fingers[2]==0:
            
            
            x3 = np.interp(x1, (frameR,wCAM-frameR), (0,wSCRN))
            y3 = np.interp(y1, (frameR,hCAM-frameR), (0,hSCRN))
            

            clocX = plocX + (x3-plocX)/smoothen
            clocY =plocY + (y3-plocY)/smoothen
    
            autopy.mouse.move(clocX,clocY)
            #autopy.mouse.move(x3,y3)
            cv2.circle(img, (x1,y1), 15, (255,0,0), cv2.FILLED)
            plocX, plocY = clocX, clocY
    
    
        if fingers[1] == 1and fingers[2]==1:
            length, img, line = detector.findDistance(8,12,img)
            
            if length <= 35:
                cv2.circle(img, (line[4], line[5]), 15, (0,255,0), cv2.FILLED)
                autopy.mouse.click()    
                
            
    cv2.imshow("image", img)
    cv2.waitKey(1)