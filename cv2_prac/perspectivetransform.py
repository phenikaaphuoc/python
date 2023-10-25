import cv2
import matplotlib.pyplot as plt

image_path = r"C:\Users\phuoc\Downloads\san_bong.jpg"

img = cv2.imread(image_path)
plt.imshow(img)

