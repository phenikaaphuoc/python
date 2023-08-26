import cv2
import torch
import numpy as np
from ultralytics import YOLO

# Path to ONNX model
model_path = r"C:\Users\phuoc\Downloads\best.pt"

input = torch.rand(1,3,640,640)

model = YOLO(model_path)
count = 0
count_line = 320
offset = 12
def get_centre(x1,y1,x2,y2):
    w_x = x2-x1
    w_y = y2-y1
    cx = int(x1+w_x/2)
    cy = int(y1+w_y/2)
    return (cx,cy)

cam = cv2.VideoCapture(r"C:\Users\phuoc\Downloads\y2mate.com - Cars Moving On Road Stock Footage  Free Download_1080p.mp4")

tracker = cv2.TrackerMIL()




while True:
    ret,image = cam.read()
    if not ret:
        break
    # image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image = cv2.resize(image,(640,640))


    tensor = torch.tensor(image[None,:,:])/255.0
    tensor = tensor.permute(0,3,1,2)
    image = cv2.line(image, (0, count_line), (640, count_line), (0, 255, 0), 1)
    output = model(tensor,verbose = False)
    boxes = output[0].boxes.xyxy.detach()
    for box in boxes:

        x1,y1,x2,y2 = torch.tensor(box,dtype=int)
        x1 = x1.item()
        y1 = y1.item()
        x2 = x2.item()
        y2 = y2.item()
        image = cv2.rectangle(image, (x1, y1), (x2, y2), (250, 0, 0), 2)
        centre = get_centre(x1,y1,x2,y2)
        if centre[1]>count_line-offset and centre[1]<count_line+offset:
            count+=1
        image = cv2.circle(image,centre,4,(0,0,255),-1)

    image = cv2.putText(image,"number vehicels: "+str(count),(20,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
    cv2.imshow("video", image)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
cam.release()
# Destroy all the windows
cv2.destroyAllWindows()