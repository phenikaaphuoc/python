import  numpy as np
import  copy
import random
random.seed(8)
np.random.seed(8)
def GCD(a, b):
    gdc = 1
    min_value = min(a,b)

    for i in range(2,min_value+1):
        if a%i==0 and b %i ==0:
            gdc = i
    return gdc

def inverseMod(a, m):
    gcd = GCD(a, m)
    if gcd != 1:
        # a không có module nghịch đảo
        return None
    else:
        return pow(a,-1,m)
class Virgen:

    def __init__(self,k):

        self.k = []

        self.map  = {}

        self.char = "abcdefghijklmnopqrstuvwxyz@-."

        for i,char in  enumerate(self.char):

            self.map[char] = i

        for char in k:
            self.k.append(self.map[char]+1)

        self.n = len(self.map)


    def encode(self,p:str):

        encode = ""
        for i,char in enumerate(p.lower()):

            if char not in self.map.keys():
                encode+= char
                continue

            value = (self.map[char] + self.k[i % len(self.k)]) % self.n

            encode += self.char[value]

        return encode

    def decode(self,e):

        p = ""
        for i, char in enumerate(e.lower()):

            if char not in self.map.keys():
                p += char
                continue

            value = (self.map[char] - self.k[i % len(self.k)])



            p += self.char[(value+self.n)%self.n]

        return p
class ceasar:
    def __init__(self,k:int):

        self.k  = k

        self.map = {}

        self.char = "abcdefghijklmnopqrstuvwxyz@-."

        for i, char in enumerate(self.char):
            self.map[char] = i

        self.n = len(self.map)

    def encode(self,p:str):

        encode = ""
        for i,char in enumerate(p.lower()):

            if char not in self.map.keys():
                encode+= char
                continue

            value = (self.map[char] + self.k) % self.n

            encode += self.char[value]

        return encode

    def decode(self, e):

        p = ""
        for i, char in enumerate(e.lower()):

            if char not in self.map.keys():
                p += char
                continue

            value = (self.map[char] - self.k)

            p+= self.char[(value+self.n)%self.n]
        return p
def find_factors(n):
    factors = []
    for i in range(2, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

class RSA:
    def __init__(self,p = 5,q = 7):
        self.map = {}

        self.char = "abcdefghijklmnopqrstuvwxyz@-."

        for i, char in enumerate(self.char):

            self.map[char] = i


        self.n = p*q

        self.phi = (p-1)*(q-1)


        factors = find_factors(self.phi)

        while True:
            check = 1
            self.e = random.randint(100,1000)
            for factor in find_factors(self.e):
                if factor in factors:
                    check = 0
            if check == 1:
                break
        print(self.e,self.n)
        self.k = pow(self.e,-1,self.phi)
    def encode_char(self,char):

        value = self.map[char]

        encode_value = pow(value,self.e) % self.n


        en_char = encode_value



        return en_char
    def encode(self,p):

        encode = []
        for char in p.lower():

            if char not in self.map.keys():
                encode+= char
                continue

            encode += [self.encode_char(char)]

        return encode
    def decode_char(self,char):


        decode_value =  pow(char,self.k) % self.n

        p_char = decode_value

        return p_char

    def decode(self,en):
        p = ""

        for char in en:


            p  += self.char[self.decode_char(char)]

        return p



class Anffine:
    def __init__(self,a,b):

        self.a = a
        self.b = b

        self.map = {}

        self.char = "abcdefghijklmnopqrstuvwxyz@-."

        for i, char in enumerate(self.char):
            self.map[char] = i

        self.k = pow(a,-1,len(self.char))

    def encode(self,p):
        en = ""

        for char in p:

            value = (self.a*self.map[char]+self.b) % len(self.char)

            en+=self.char[value]

        return en

    def decode(self,en):

        de = ""

        for char in en:
            value = (self.k * (self.map[char] - self.b + len(self.char)) % len(self.char))
            de += self.char[value]
        return de
class Des:
    def __init__(self):

        self.hv64 = np.arange(64)
        np.random.shuffle(self.hv64)

        self.key = np.random.randint(0,1+1,64)

        self.bkkl = np.array([i for i in range(64) if (i+1)%8!=0 or i ==0 ])
        np.random.shuffle(self.bkkl)

        self.so_dich = np.random.randint(1,2+1,16)

        self.nen = np.arange(56)
        np.random.shuffle(self.nen)
        self.nen = self.nen[:48]

        self.morong = np.arange(32)
        lap = np.random.randint(0,31+1,16)
        self.morong = np.concatenate([self.morong,lap],axis=0)
        np.random.shuffle(self.morong)

        self.init_box_s()



    def encode_64(self,bit):

        hv64 = self.hoan_vi_64(bit)

        trai,phai = hv64[:32],hv64[32:]


        key_56 = self.bo_key_kiem_loi()

        key_trai,key_phai = key_56[:28],key_56[28:]

        for i in range(16):

            so_dich_trai = self.so_dich[i]


            key_trai_new,key_phai_new  = self.dich_trai(key_trai,so_dich_trai),self.dich_trai(key_phai,so_dich_trai)

            key_new =np.concatenate([key_trai_new,key_phai_new],axis=0)

            key_new = key_new[self.nen]

            phai = phai[self.morong]


            phai = np.bitwise_xor(key_new,phai)


    def init_box_s(self):

        self.box_s = []
        for i in range(8):
            s = np.random.randint(0,15,(4,16))
            self.box_s.append(s)
    def bit_to_dec(self,bits):

        value = 0
        for i,bit in enumerate(bits[::-1]):
            value+= bit*pow(2,i)
        return value

    def dec_to_bit(self,hex,num = 4):

        bits = []
        while hex!=0:

            bits.append(hex%2)
            hex = hex//2
        num = num - len(bits)
        bits = [0] * num+ bits
        return bits[::-1]


    def BOXS(self,bits):

        new_bits = []
        for i in range(8):
            bit = bits[i*6:(i+1)*6]

            row = self.bit_to_dec([bit[0],bit[-1]])
            col = self.bit_to_dec(bit[1:-1])


            value = self.box_s[i][row,col]

            new = self.dec_to_bit(value)

            new_bits+= new

        return new_bits






    def bo_key_kiem_loi(self):

        k = np.copy(self.key)

        return k[self.bkkl]

    def dich_trai(self,k,n):

        k = np.copy(k)

        k[: k.shape[0] -n ] = k[n: ]
        k[k.shape[0]-n : ] = [0]*n

        return k




    def encode(self,p):

        pass

    def decode(self,en):

        pass
    def hoan_vi_64(self,ma):

        ma = np.copy(ma)

        ma = ma[self.hv64]

        return ma


import hashlib

def string_to_bits(input_string):
    # Chuyển đổi mỗi ký tự thành mã ASCII và sau đó thành dãy bit
    bits = ''.join(format(ord(char), '08b') for char in input_string)
    return bits
def calculate_md5(input_string):
    # Encode the input string to bytes
    input_bytes = input_string.encode('utf-8')

    # Calculate the MD5 hash
    md5_hash = hashlib.md5(input_bytes).hexdigest()

    return md5_hash


def pad_to_512_bits(bits):
    # Bước 1: Xác định số bit cần thêm để đạt đủ 512 bit
    padding_length = 512 - (len(bits) % 512)

    # Bước 2: Thêm một bit '1'
    bits += '1'

    # Bước 3: Thêm các bit '0' cho đến khi đạt kích thước cần thiết
    bits += '0' * (padding_length - 1)

    # Bước 4: Thêm 64 bit để biểu diễn độ dài ban đầu của chuỗi (sử dụng 64 bit thể hiện độ dài)
    original_length_bits = '{:064b}'.format(len(bits))
    bits += original_length_bits

    return bits


# Chuỗi cần chuyển đổi thành dãy bit
input_string = "Hello, world!"

# Chuyển đổi thành dãy bit
bits = string_to_bits(input_string)

# Đệm để đạt đủ 512 bits
padded_bits = pad_to_512_bits(bits)

# In dãy bit đã được đệm
print("Dãy bit sau khi đệm:", padded_bits)

# model = Des()
# hv64 = model.hoan_vi_64(np.arange(64))
# model.encode_64(np.random.randint(0,1+1,64))
# model.BOXS(np.random.randint(0,1+1,48))
