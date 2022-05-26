from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import HandTrackingModule as htm
import numpy as np
import time
import math
import cv2


detector = htm.handDetector(detectionCon=0.7)
cap = cv2.VideoCapture(1)

ptime = 0
ctime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList, _ = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        length = math.hypot(x2 - x1, y2 - y1)


        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volume.SetMasterVolumeLevel(vol, None)


    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("IMAGE", img)
    if cv2.waitKey(1) == ord('q'):
        break
