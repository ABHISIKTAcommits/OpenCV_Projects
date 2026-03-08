#cmd -> py -3.11 VolumeChg.py

import cv2
import time 
import numpy as np
import math
import HandTrackModule as htm
import screen_brightness_control as sbc
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) 
pTime=0
detector = htm.handDetector(detectionCon=0.7)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
speakers = AudioUtilities.GetSpeakers()
interface = speakers.EndpointVolume
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

print(minVol, maxVol)
vol = 0
volBar = 400
volPer = 0
brightness = 0
brightBar = 400
brightPer = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    cv2.rectangle(img, (300, 80), (600, 120), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "LEFT HAND = VOLUME", (320, 110), cv2.FONT_HERSHEY_PLAIN, 1.5, (57, 255, 20), 1)
    cv2.rectangle(img, (300, 130), (650, 170), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "RIGHT HAND = BRIGHTNESS", (320, 160), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 1)
    if len(lmList) != 0:
        if lmList[20][1] > lmList[17][1]:
            cv2.putText(img, "VOLUME ACTIVE", (330, 70), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,0), 2)
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 15, (57, 255, 20), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (57, 255, 20), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            pulse = int(5 + (volPer/100)*10)
            if 50 <= length <= 300:
                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)
            if length < 40:
                volume.SetMute(1, None)   
            else:
                volume.SetMute(0, None)   
            if length < 50:
                cv2.circle(img, (cx, cy), 15, (57, 255, 20), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            for i in range(8, 0, -2):
                cv2.rectangle(img, (50-i, 150-i), (85+i, 400+i), (255, 0, 0), 1)
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 2)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (57,255,20), cv2.FILLED)
            cv2.putText(img, f'VOLUME: {int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 0.7, (57, 255, 20), 2)
        else:
            cv2.putText(img, "BRIGHTNESS ACTIVE", (330, 70), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,0), 2)
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 15, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 255, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)
            brightness = np.interp(length, [50, 300], [0, 100])
            brightBar = np.interp(length, [50, 300], [400, 150])
            brightPer = np.interp(length, [50, 300], [0, 100])
            if 50 <= length <= 300:
                sbc.set_brightness(int(brightness))
            if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            for i in range(8, 0, -2):
                cv2.rectangle(img, (150-i, 150-i), (185+i, 400+i), (255, 0, 0), 1)
            cv2.rectangle(img, (150, 150), (185, 400), (255, 0, 0), 2)
            cv2.rectangle(img, (150, int(brightBar)), (185, 400), (0,255,255), cv2.FILLED)
            cv2.putText(img, f'BRIGHTNESS: {int(brightPer)} %', (140, 450), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2)
    
    cv2.rectangle(img, (20, 60), (260, 100), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "Press 'q' to quit", (30, 84), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    cv2.imshow("Hand Tracking - Volume (Left) & Brightness (Right)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()