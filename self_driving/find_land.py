import cv2
import matplotlib
import os

image_path = "HIGH_WAY.jpg"
image = cv2.imread(image_path)
blured = cv2.GaussianBlur(image,(5,5),0)
gray = cv2.cvtColor(blured,cv2.COLOR_RGB2GRAY)

edges = cv2.Canny(gray,80,200)
cv2.imshow("image",image)
cv2.imshow("edges",edges)
print(image.shape)
cv2.waitKey(10000)
cv2.destroyAllWindows()