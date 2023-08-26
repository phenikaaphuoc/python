import cv2

path_image = r"Screenshot 2023-08-25 111652.png"

image = cv2.imread(path_image)
image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
image = cv2.adaptiveThreshold(image,)
image = cv2.bitwise_not(image)

