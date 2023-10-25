import cv2
import matplotlib.pyplot as plt
import numpy as np
image_path = r"C:\Users\phuoc\OneDrive\Pictures\quang_cao.jpg"

img = cv2.imread(image_path)
img_size = (510,680)
img = cv2.resize(img,img_size)

# blur_img =  cv2.GaussianBlur(img,(5,5),0)
# gray = cv2.cvtColor(blur_img,cv2.COLOR_RGB2GRAY)
#
# th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
# cv2.imshow("haha",th3)
# cv2.waitKey(3000)
#
tl = np.array([151,141])
bl = np.array([144,533])

tr = np.array((336,89))
br = np.array((328,534))

width_top = np.sqrt(pow(tl-tr,2).sum())
width_bottom = np.sqrt(pow(bl-br,2).sum())
width = int(max(width_bottom,width_top))

height_left = np.sqrt(pow(tl-bl,2).sum())
height_right = np.sqrt(pow(tr-br,2).sum())
# width = max(width_bottom,width_top)
height = int(max(height_right,height_left))
pt1 = [tl,bl,tr,br]

pt1 = np.array([tl,bl,tr,br],dtype=np.float32)
pt3 = np.array([(0,0),(0,height-1),(width-1,0),(width-1,height-1)],dtype=np.float32)


perspective2 = cv2.getPerspectiveTransform(pt1,pt3)
new_frame2 = cv2.warpPerspective(img,perspective2,(width,height),flags=cv2.INTER_LINEAR)
# new_frame2 = cv2.resize(new_frame2,(400,400))


cv2.imshow("2",new_frame2)
cv2.waitKey(10000)