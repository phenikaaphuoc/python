import cv2
import matplotlib.pyplot as plt
import numpy as np
import math
import torch
import glob
from PIL import Image
class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=7)
        self.batch1 = torch.nn.BatchNorm2d(10)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=9,bias = False)
        self.batch2 = torch.nn.BatchNorm2d(20)
        self.fc1 = torch.nn.Linear(980, 256)
        self.batch3 = torch.nn.BatchNorm1d(256)
        self.dropout1 = torch.nn.Dropout(0.3)
        self.fc2 = torch.nn.Linear(256,10 )
    def forward(self, x):
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv1(x), 2))
        x = self.batch1(x)
        x = torch.nn.functional.relu(torch.nn.functional.max_pool2d(self.conv2(x), 2))
        x = self.batch2(x)
        x = x.view(-1, 980)
        x = torch.nn.functional.relu(self.fc1(x))
        x = self.dropout1(x)
        x = self.fc2(x)
        return x
def read_gray(path_image):
    image = cv2.imread(path_image)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image,(3,3),5)
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    image = cv2.bitwise_not(image)
    origin_image = np.copy(image)
    gray_image = cv2.erode(image,np.ones((3,3),dtype = int),iterations=2)
    return gray_image,origin_image
def find_board(image,origin_image):
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key = cv2.contourArea,reverse=True)
    board = None
    for contour in contours:
      if cv2.contourArea(contour) > image.shape[0] * image.shape[1]* 0.1:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4 :
          board_cnf = approx
          board = np.array(approx).squeeze()
          break

    board = board[np.argsort(board[:,0])]
    lefts = board[:2]
    lefts = lefts[np.argsort(lefts[:,1])]
    tl,bl = lefts[0], lefts[1]
    rights = board[2:]
    rights = rights[np.argsort(rights[:,1])]
    tr,br = rights[0],rights[0]
    roi = origin_image[tl[1]:bl[1],tl[0]:tr[0]]

    # plt.imshow(image[tl[1]:bl[1],tl[0]:tr[0]])

    return board_cnf,roi
def extract_cell(path_image):

    gray_image,origin_image = read_gray(path_image)
    board_cnf,roi = find_board(gray_image,origin_image)

    length = int(math.sqrt(cv2.contourArea(board_cnf)/82))
    count = 1
    plt.figure(figsize = (6,10))
    margin_vertical = 10
    margin_horizal = 15
    cell_datas = []
    mask = []
    for i in range(9):
      for j in range(9):

        cell = roi[length*i+margin_vertical:length*(i+1)-margin_vertical,length*j+margin_horizal:length*(j+1)-margin_horizal]
        cell = cv2.resize(cell,(50,50))
        cell = cv2.erode(cell,(5,5),2)

        if np.sum(np.where(cell==0,0,1))>80:
            mask.append(False)
        else:
            mask.append(True)

        cell_datas.append(torch.tensor(cell/255.0,dtype = torch.float32).unsqueeze(0).unsqueeze(0))

        # plt.subplot(9,9,count)
        # plt.imshow(cell,cmap = 'gray')
        # plt.xticks([])
        # plt.yticks([])
        count+=1
    return cell_datas,mask
class Solver:
    def __init__(self,model_path,device = 'cpu'):
        self.model = torch.load(model_path,map_location=torch.device('cpu'))
        self.device = device

    def predict(self,data_cell,mask):
        data_cell = torch.cat(data_cell,0).to(self.device)

        value = self.model(data_cell)

        _ , number = value.max(1)
        number[mask] = 0
        return number

    def solve(self,image_path):

        data_cell,mask  = extract_cell(image_path)
        numbers = self.predict(data_cell,mask)
        print(numbers)
solver = Solver(r"D:\python\sodoku\predict_number.pt")
solver.solve(r"D:\python\sodoku\Screenshot 2023-08-25 111652.png")