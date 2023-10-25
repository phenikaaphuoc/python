
import keyboard
import  cv2

eye_detect = cv2.CascadeClassifier("haarcascade_eye.xml")
face_detect = cv2.CascadeClassifier("haarcascade_frontalcatface.xml")



cap = cv2.VideoCapture(0)
while True:
    if keyboard.is_pressed("q"):
        print("out")
        break
    ret ,img = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

    faces = face_detect.detectMultiScale(gray)
    eyes = eye_detect.detectMultiScale(gray)
    for face in faces:
        x,y,w,h = face
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(255,0,0),thickness=3)
    for eye in eyes:
        x,y,w,h = eye
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,255,0),thickness=3)


    cv2.imshow("hand",img)
    cv2.waitKey(8)