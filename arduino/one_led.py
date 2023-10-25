import cv2
import  mediapipe as mp
cap = cv2.VideoCapture()
cap.open("http://192.168.0.104:81/stream")
mp_face_detection = mp.solutions.face_detection.FaceDetection()
def draw_rec(image,rec):

    imag_shape= image.shape[:2][::-1]



    if rec[0]<=1:

        rec = [ int(imag_shape[i%2]*rec[i]) for i,value in  enumerate(rec)]

    x,y,w,h = rec

    pt1 = (x,y)
    pt2 = (x+w,y+h)

    image = cv2.rectangle(image,pt1,pt2,color=(255,0,0),thickness=1)

    return image

try:
    while(True):
         # Capture frame-by-frame
        if not cap.isOpened():
            break
        ret, frame = cap.read()


        if not ret :

            break

        results = mp_face_detection.process(frame)
        if results.detections:

            # print(results.detections)
            for detection in results.detections:

                score = detection.score

                if score[0] > 0.7:

                    relative_bouding_box = detection.location_data.relative_bounding_box

                    x_min = relative_bouding_box.xmin

                    y_min = relative_bouding_box.ymin
                    width = relative_bouding_box.width
                    height = relative_bouding_box.height

                    relative_bouding_box = [x_min,y_min,width,height]
                    frame = draw_rec(frame,relative_bouding_box)
                    break


        # Display the resulting frame
        cv2.imshow('Salida',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture


except Exception as e:
    print("An exception occurred:", str(e))
    cap.release()
    cv2.destroyAllWindows()
finally:
    # When everything is done or an exception occurs, release the capture and destroy the window
    cap.release()
    cv2.destroyAllWindows()