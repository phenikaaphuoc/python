import numpy as np
np.random.seed(8)
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

        self.hv32 = np.arange(32)
        np.random.shuffle(self.hv32)

        self.hvcuoi = np.arange(64)
        np.random.shuffle(self.hvcuoi)

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

            phai_cu = np.copy(phai)
            phai = phai[self.morong]



            phai = np.bitwise_xor(key_new,phai)

            phai = self.BOXS(phai)



            phai = np.bitwise_xor(phai,trai)
            trai = phai_cu

        encode = np.concatenate([trai,phai],axis=0)
        encode = encode[self.hvcuoi]
        return encode

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


        bits = []
        for char in p.replace(" ",""):
            ascii_value = ord(char)

            binary_value = bin(ascii_value)

            bits+= [int(bit) for bit in binary_value[2:].zfill(8)]

        num_paddings = 64-len(bits)%64
        bits += [0] *num_paddings

        encodes = []
        for i in range(len(bits)//64):

            bit = bits[i*64:(i+1)*64]

            encodes+=self.encode_64(bit).tolist()

        chars = ""
        with open("des-encrypt.dat",'w',encoding='utf-8') as f:
            for i in range(len(encodes)//8):

                bit =  [ str(new) for new in encodes[i*8:(i+1)*8]]

                binary_str =  "".join(bit)

                decimal_value = int(binary_str, 2)


                char_value = chr(decimal_value)
                chars+= char_value
                f.write(char_value)










    def hoan_vi_64(self,ma):

        ma = np.copy(ma)

        ma = ma[self.hv64]

        return ma



model = Des()
model.encode("I love Phenikaa")

