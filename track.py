import cv2
import math
class Traker:
    def __init__(self,distance_thredsold = 10):
        self.tracks = {}
    def update(self,boxes):
        if len(self.tracks==0):
            for i,box in enumerate(boxes):
                self.tracks[i] = box
                