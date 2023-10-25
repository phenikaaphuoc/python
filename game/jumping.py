import time

import keyboard
import numpy as np

from  capture_jumping import Capture
import cv2
from pynput.keyboard import Key, Controller

class Khung_Long:
    def __init__(self):

        self.cap = None
        self.tem_plate = cv2.imread("khung_long.png",cv2.IMREAD_GRAYSCALE)
        self.my_keyboard = Controller()
        while not self.cap:
            self.cap = Capture("Crôm Dino Trò Chơi Trực Tuyến - Google Chrome")

            if self.cap.window :
                while True:
                    start = input("press s to start: ")
                    if start == 's':
                        self.custom_init()
                        if self.ret:
                            self.solve()
                        break
    def press(self,key,delay = 0.1):
        self.my_keyboard.press(key)
        time.sleep(delay)
        self.my_keyboard.release(key)
    def custom_init(self):
        self.cap.active()
        self.press(Key.f5,0.08)
        time.sleep(2)
        self.press(Key.space,0.08)
        time.sleep(1)
        img,ret = self.cap.take_screenshot()

        if not ret :
            self.ret = False
            return
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        h, w = self.tem_plate.shape[:2]

        res = cv2.matchTemplate(gray, self.tem_plate, cv2.TM_CCOEFF_NORMED)
        _,value,_,min_loc = cv2.minMaxLoc(res)
        self.ret = value>0.8

        self.loc_kl = (min_loc[0],min_loc[1])




        # cv2.rectangle(gray, min_loc, (min_loc[0] + w, min_loc[1] + h), 0, 2)


        new_img = gray[min_loc[1]-300:min_loc[1]+200,:]
        ret,thresh = cv2.threshold(new_img,250,255,0)

        contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours,key = cv2.contourArea,reverse=True)

        x,y,w,h = cv2.boundingRect(contours[1])


        self.board = [x,min_loc[1]-300+y,w,h]
        print("san sang")

        # x,y,w,h = self.board
        # new_img =img[y:y+h,x:x+w]
        # cv2.imshow("hhe",new_img)
        # cv2.waitKey(30000)
        # cv2.destroyAllWindows()
    def take_board(self):

        img, ret = self.cap.take_screenshot()

        if not ret:
            return None,False
        x,y,w,h = self.board
        img = img[y:y+h,x:x+w//2,:]

        return  img,True


    def solve(self):

        while True:

            # before = time.time()

            img,ret = self.take_board()
            gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
            if gray[10,10]==13:
                gray = cv2.bitwise_not(gray)
            elif gray[10,10] != 242:
                continue
            ret,thresh = cv2.threshold(gray,200,255,0)
            cnts ,_= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts = [cv2.boundingRect(cnt)  for cnt in cnts if cv2.contourArea(cnt)>80]
            cnts = [cnt for cnt in cnts if cnt[3]>20 and cnt[0] > 20]
            # image = np.zeros_like(gray,np.uint8)
            cnts = sorted(cnts, key=lambda x: x[0])
            if keyboard.is_pressed("q"):
                print(gray[10,10])
                break

            # #
            # for cnt in cnts:
            #     cv2.rectangle(image, (cnt[0], cnt[1]), (cnt[0] + cnt[2], cnt[1] + cnt[3]), 255, 3)
            # # if len(cnts)>1:
            #     cv2.putText(image,str(cnt[0]),(cnt[0],cnt[1]),2,2,255,2)

            # cv2.imshow("ga",image)
            if len(cnts)>1:
                next = cnts[1]
                curent = cnts[0]

                distance_ratio = (next[0]-curent[0]) / 350


                if distance_ratio<1:
                    if next[1]+next[3]*2//3 < curent[1]+30:
                        self.press(Key.down,distance_ratio*0.5)
                    else:
                        self.press(Key.up,distance_ratio*0.9/2)


            #
            #     print(cnts[1][0] -cnts[0][0])
            # cv2.imshow("hi",image)
            # cv2.waitKey(8)
            #
            # print(1/(time.time() - before))



kl = Khung_Long()
# Capture.enum_window_titles()