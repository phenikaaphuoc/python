from cvzone.HandTrackingModule import HandDetector
import keyboard
import  cv2


detector = HandDetector(detectionCon=0.8,)


cap = cv2.VideoCapture(0)
while True:
    if keyboard.is_pressed("q"):
        print("out")
        break
    ret ,img = cap.read()
    hands, img = detector.findHands(img, draw=True)
    print(hands[0])
    cv2.imshow("hand",img)
    cv2.waitKey(8)
