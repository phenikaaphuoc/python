def encode(p,k= 3):

    if k<=0 or k>126-32:
        raise "mã k không hợp lệ"

    e = ""
    for i in p.lower().replace(" ",""):

        hash_value = ord(i) + k

        # if i.isdigit():
        #
        #     if hash_value>57:
        #         hash_value = hash_value%57+48
        # elif i.isalpha():
        #
        #     if hash_value>122:
        #         hash_value = hash_value%122+97
        #
        if hash_value>126:
            hash_value = hash_value%126 + 32

        e+=chr(hash_value)

    return e
def decode(e,k = 3):
    if k<=0 or k>126-32:
        raise "mã k không hợp lệ"
    d= ""
    for i in e:
        hash_value = ord(i)-k
        if hash_value<32:
            hash_value = (126-(32-hash_value))
        d+=chr(hash_value)

    return d

print()
p = input("Nhap vao bản rõ: ")
k =int(input("Nhap vao ma k: "))

print("encode ban vua nhap: ",encode(p,k))
print("decode: ",decode(encode(p,k),k))
print()
with open("data.txt",'r') as f:
    data = f.read().strip()
    print("clear text trong file data.txt: ",data)
    print("encode trong file data.txt: ",encode(data,k))
    print("decode: ",decode(encode(data,k),k))