import cv2
from time import sleep
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ]

finalText = ""

keyboard = Controller()


# def drawAll(img, buttonList):
#     imgCanvas = np.zeros((720, 1280, 3), np.uint8)
#     imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
#     _, imgInv = cv2.threshold(imgGray, 50,255, cv2.THRESH_BINARY_INV) #50,255
#     imgBGR = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
#     imgAND = cv2.bitwise_and(img, imgBGR)
#     imgOR = cv2.bitwise_or(imgAND, imgCanvas)
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#         cv2.rectangle(imgOR, button.pos, (x + w, y + h), (192, 192, 192), cv2.FILLED)
#         cv2.putText(imgOR, button.text, (x + 10, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#     return imgOR

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (192, 192, 192), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    return img


class Button():
    def __init__(self, pos, text, size=[80, 80]):
        self.pos = pos
        self.text = text
        self.size = size


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([j*100+50, 100*i+50], key))

while True:
    success, img1 = cap.read()
    img = cv2.flip(img1, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            # checking the location of index finger and adding hover effect
            if x < lmList[8][0] < x+w and y < lmList[8][1] <y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (160, 160, 160), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

                l, _, _ = detector.findDistance(8, 4, img,draw=True)
                # print(l)
                # when clicked
                if l < 30:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)

                    finalText += button.text
                    sleep(0.20)

    # cv2.rectangle(img, (50, 550), (700, 450), (160, 160, 160), cv2.FILLED)
    # cv2.putText(img, finalText, (60, 525), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
