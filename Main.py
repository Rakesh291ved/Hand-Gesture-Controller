import cv2
import numpy as np
import time
import pyautogui
import math
import HandTrackingModule as htm

#################################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

scroll_mode = False
vol_mode = False
cursor_mode = False
mode = 'None'
#################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
ptime = 0

wScr, hScr = pyautogui.size()  # Screen size

def fingers_up(lmList):
    fingers = []
    tipIds = [4, 8, 12, 16, 20]
    if len(lmList) == 0:
        return []

    # Thumb
    fingers.append(1 if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] else 0)
    # 4 Fingers
    for id in range(1, 5):
        fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)
    return fingers

def draw_info(img, mode):
    cv2.rectangle(img, (0, 0), (150, 80), (255, 255, 255), -1)
    cv2.putText(img, f'{mode}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 255), 2)

def scroll_mode_action(img, lmList):
    if len(lmList) != 0:
        y1 = lmList[8][2]
        y2 = lmList[12][2]
        fingers = fingers_up(lmList)
        if fingers == [0, 1, 1, 0, 0]:
            if abs(y1 - y2) > 40:
                pyautogui.scroll(20)
            elif abs(y1 - y2) < 10:
                pyautogui.scroll(-20)
            cv2.putText(img, 'Scroll', (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def volume_mode_action(img, lmList):
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [30, 300], [0, 100])
        pyautogui.press("volumedown") if vol < 50 else pyautogui.press("volumeup")
        cv2.putText(img, f'Volume: {int(vol)}', (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def cursor_mode_action(img, lmList):
    global plocX, plocY, clocX, clocY
    if len(lmList) != 0:
        x1, y1 = lmList[8][1], lmList[8][2]
        fingers = fingers_up(lmList)
        if fingers == [0, 1, 0, 0, 0]:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    fingers = fingers_up(lmList)

    # Mode switching gesture: All fingers folded
    if fingers == [0, 0, 0, 0, 0]:
        mode = 'Scroll'
    elif fingers == [1, 1, 0, 0, 0]:
        mode = 'Volume'
    elif fingers == [0, 1, 0, 0, 0]:
        mode = 'Cursor'

    draw_info(img, mode)

    if mode == 'Scroll':
        scroll_mode_action(img, lmList)
    elif mode == 'Volume':
        volume_mode_action(img, lmList)
    elif mode == 'Cursor':
        cursor_mode_action(img, lmList)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f'FPS: {int(fps)}', (500, 70), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
