import cv2
import keyboard
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import copy


hand_detector = HandDetector(detectionCon=0.8)
class Solver:
    def __init__(self):
        self.img_size = (790,400)
        self.cap  = cv2.VideoCapture(0)
        self.initTransform()
        self.initLocationChar()
        self.solve()
        # self.hand_detector = HandDetector(detectionCon=0.8)



    def initLocationChar(self):

        self.row_gap = 20
        self.col_gap = 20
        self.chars = {}
        self.begin = (80,80)
        x, y = self.begin
        self.width_cell = 50
        self.height_cell = 50
        self.press_value = np.zeros(self.img_size[::-1])

        row1 = ['q','w','e','r','t','y','u','i','o','p']
        row2 = ['a','s','d','f','g','h','j','k','l']
        row3 =  ['z','x','c','v','b','n','m']


        self.rows = [row1,row2,row3]
        for col,row in enumerate(self.rows):


            x = self.begin[0]
            x+= (len(self.rows[0]) - len(self.rows[col]))*(self.width_cell+self.row_gap)//2

            for i,char in enumerate(row):

                self.chars[char] = (x,y)


                self.press_value[y:y+self.height_cell+1,x:x+self.width_cell+1] = np.full((self.height_cell+1,self.width_cell+1),fill_value=ord(char))


                x+= self.width_cell+self.row_gap

            y+= self.height_cell+self.col_gap

    def initTransform(self):

        w,h = self.img_size
        tl = (0, 0)
        tr = (w, 0)
        bl = (0, h)
        br = (w, h)
        pt1 = np.array([tl, tr, bl, br], np.float32)
        pt2 = np.array([tr, tl, br, bl], np.float32)
        self.matrix = cv2.getPerspectiveTransform(pt1, pt2)
    def drawRectangle(self,img,location:tuple,char:str):

        x1,y1 = location
        x2,y2 = x1+50,y1+50
        img = cv2.rectangle(img,location,(x2,y2),color=(255,0,0),thickness=2)
        img = cv2.putText(img,  str(char),(x1+10,y1+35), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
        return  img
    def drawAll(self,img):

        for char in self.chars.keys():
            self.drawRectangle(img,self.chars[char],char)

    def solve(self):
        w,h = self.img_size
        while True:

            if keyboard.is_pressed("q"):
                print("out")
                cv2.destroyAllWindows()
                break

            ret, img = self.cap.read()
            if not ret:
                print("Something wrong")
                break
            img = cv2.resize(img,(w,h))

            img = cv2.warpPerspective(img,self.matrix,(w,h),flags=cv2.INTER_LINEAR)
            hands, _ = hand_detector.findHands(img, flipType=False,draw=False)

            if hands:
                hand = hands[0]['lmList']
                points = hand[8][:2]
                points2 = hand[12][:2]

                value1 = self.press_value[points[1],points[0]]
                value2 = self.press_value[points2[1],points2[0]]
                if value1 == value2:
                    if value1!=0:
                        print("press: ",chr(int(value1)))

                cv2.circle(img,points,color=(255,0,0),thickness=-1,radius=10)
                cv2.circle(img,points2,color=(255,0,0),thickness=-1,radius=10)

            self.drawAll(img)
            cv2.imshow("image",img)
            cv2.waitKey(8)

solver = Solver()