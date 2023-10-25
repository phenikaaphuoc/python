import  numpy as np
import  copy
import random


class Virgen:

    def __init__(self,k):

        self.k = []

        self.map  = {}

        self.char = "abcdefghijklmnopqrstuvwxyz@-."

        for i,char in  enumerate(self.char):

            self.map[char] = i+1

        for char in k:
            self.k.append(self.map[char])

        self.n = len(self.map)


    def encode(self,p:str):

        encode = ""
        for i,char in enumerate(p.lower()):

            if char not in self.map.keys():
                encode+= char
                continue

            value = (self.map[char] + self.k[i % len(self.k)]) % self.n

            encode += self.char[value-1]

        return encode

    def decode(self,e):

        p = ""
        for i, char in enumerate(e.lower()):

            if char not in self.map.keys():
                p += char
                continue

            value = (self.map[char] - self.k[i % len(self.k)])

            if value <=0:
                value += self.n

            p += self.char[value - 1]

        return p
class ceasar:
    def __init__(self,k:int):

        self.k  = k

        self.map = {}

        self.char = "abcdefghijklmnopqrstuvwxyz@-."

        for i, char in enumerate(self.char):
            self.map[char] = i + 1

        self.n = len(self.map)

    def encode(self,p:str):

        encode = ""
        for i,char in enumerate(p.lower()):

            if char not in self.map.keys():
                encode+= char
                continue

            value = (self.map[char] + self.k) % self.n

            encode += self.char[value-1]

        return encode

    def decode(self, e):

        p = ""
        for i, char in enumerate(e.lower()):

            if char not in self.map.keys():
                p += char
                continue

            value = (self.map[char] - self.k)

            if value <= 0:
                value += self.n

            p += self.char[value - 1]

        return p

model = ceasar(3)
print(model.encode("kk"))
print(model.decode("nn"))




