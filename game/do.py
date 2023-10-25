import cv2
import numpy as np





lower_sky_blue = np.array([90, 50, 50])  # Lower HSV values for sky blue
upper_sky_blue = np.array([130, 255, 255])  # Upper HSV values for sky blue
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)

text_position = (150, 150)
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (255, 255, 255)
font_thickness = 2

cap = cv2.VideoCapture(r"C:\Users\phuoc\Downloads\video.mp4")
def do_dai(pt1,pt2):
    x1,x2 = pt1
    x3,x4 = pt2

    return np.sqrt(pow(x3-x1,2)+pow(x4-x2,2))

while True:

    ret,img = cap.read()

    if not ret:
        break

    img = cv2.resize(img, (448, 448))

    # img = cv2.GaussianBlur(img, (11, 11), 0)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(img_hsv, lower_sky_blue, upper_sky_blue)
    mask2 = cv2.inRange(img_hsv,lower_skin,upper_skin)


    sky_blue_object = cv2.bitwise_and(img, img, mask=mask)
    yellow_object = cv2.bitwise_and(img,img,mask= mask2)

    gray_card = cv2.cvtColor(sky_blue_object,cv2.COLOR_BGR2GRAY)
    gray_hand = cv2.cvtColor(yellow_object,cv2.COLOR_BGR2GRAY)

    ret,gray_card = cv2.threshold(gray_card,100,255,cv2.THRESH_BINARY)
    ret,gray_hand = cv2.threshold(gray_hand,150,255,cv2.THRESH_BINARY)

    conts,_ = cv2.findContours(gray_card,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    card = sorted(conts,key=lambda x:cv2.contourArea(x),reverse=True)[0]

    epsilon = 0.02 * cv2.arcLength(card, True)
    card_approx = cv2.approxPolyDP(card, epsilon, True)

    conts,_ = cv2.findContours(gray_hand,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    hand = sorted(conts,key=lambda x:cv2.contourArea(x),reverse=True)[0]

    hull = cv2.convexHull(card_approx)

    extreme_points = sorted(hull[:, 0],key=lambda x:x[0]+x[1])

    top_left_board,bottom_right_board = extreme_points[0],extreme_points[-1]

    extreme_points = sorted(extreme_points,key=lambda x:x[0]-x[1])

    bottom_left_board,top_right_board = extreme_points[0],extreme_points[-1]

    width = str(int(do_dai(top_left_board,top_right_board)))
    height = str(int(do_dai(top_left_board,bottom_left_board)))

    box = cv2.boundingRect(hand)
    x1_hand,x2_hand,w_hand,h_hand = box

    gray = cv2.cvtColor(img[x2_hand:x2_hand+h_hand+1,x1_hand:x1_hand+w_hand+1],cv2.COLOR_BGR2GRAY)

    _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)
    conts,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    hand = sorted(conts,key=lambda x : cv2.contourArea(x))[-1]
    hull_2 = cv2.convexHull(hand)[:,0]+ np.array([x1_hand,x2_hand])

    hull_2 = sorted(hull_2,key= lambda  x: x[0]+x[1])

    top_left= hull_2[0].tolist()
    bottom_right = hull_2[-1].tolist()

    cv2.circle(img, tuple(top_left), 5, (0, 0, 255), -1)
    cv2.circle(img,tuple(bottom_right),3,(0,0,255),-1)

    hull_2 = sorted(hull_2,key= lambda  x: x[0]-x[1])

    top_right = hull_2[0].tolist()
    bottom_left = hull_2[-1].tolist()


    cv2.circle(img, tuple(top_right), 5, (0, 0, 255), -1)
    cv2.circle(img,tuple(bottom_left),3,(0,0,255),-1)


    eps_hand = 0.02*cv2.arcLength(hand,True)
    hand = cv2.approxPolyDP(hand,eps_hand,closed=True)

    cv2.drawContours(img, [hull], -1, (0, 255, 0), 2)

    contour_to_draw = np.array([[bottom_left], [bottom_right], [top_right], [top_left]]).reshape((-1,1,2))
    cv2.polylines(img, [contour_to_draw], isClosed=True, color=(0, 255, 0), thickness=2)



    for point in extreme_points:
        cv2.circle(img, tuple(point), 5, (0, 0, 255), -1)

    cv2.putText(img, f"w: {width} , h: {height}", top_left_board, font, font_scale, font_color, font_thickness)
    width_hand = int(do_dai(top_left,top_right))
    height_hand = int(do_dai(top_left,bottom_left))
    cv2.putText(img, f"w: {height_hand} , h: {width_hand}", top_right, font, font_scale, font_color, font_thickness)

    cv2.imshow('Original Image', img)


    if cv2.waitKey(8)==ord('q'):
        break
cv2.destroyAllWindows()
