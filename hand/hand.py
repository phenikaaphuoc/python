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

    for hand in hands:

        keypoints= hand['lmList']

        for keypoint in keypoints:

            x,y,_ = keypoint

        # Each points in keypoints is  a list [x,y,visiable]

        # Poisition of keypoints you can find in https://www.bing.com/ck/a?!&&p=bda51c73c1c1e709JmltdHM9MTY5ODE5MjAwMCZpZ3VpZD0xYzAxODE3Yi02MjA4LTZlYWMtMDI5Yi05MjNkNjMxYTZmNmUmaW5zaWQ9NTQ1NA&ptn=3&hsh=3&fclid=1c01817b-6208-6eac-029b-923d631a6f6e&u=a1L2ltYWdlcy9zZWFyY2g_cT1rZXlwb2ludCtoYW5kJmlkPTk0RTc2MjIxQTM3NzdFOTM0MkI2RUU3NUFBQTMzMzdCMDBBQ0ZFMUYmRk9STT1JUUZSQkE&ntb=1
        # Phuocsiuu
    cv2.imshow("hand",img)
    cv2.waitKey(8)
