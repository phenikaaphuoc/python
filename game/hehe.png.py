import cv2
img = cv2.imread("dem.png",cv2.IMREAD_GRAYSCALE)
img = cv2.bitwise_not(img)
ret, thresh = cv2.threshold(img, 200, 255, 0)


cv2.imshow("hehe",thresh)
cv2.waitKey(5000)
cv2.destroyAllWindows()