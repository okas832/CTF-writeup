import itertools
from Crypto.Cipher import AES

f = open("Flag.text.abcdefghm", "rb").read()

"""
for key in itertools.product(b"\x01\x02\x03\x04", repeat = 8):
    for iv in itertools.product(b"\xF8\xF9\xFA\xFB", repeat = 4):
        key = bytes(key)
        iv = bytes(iv)
        cipher = AES.new(key + b"\x00" * 8, mode = AES.MODE_CBC, iv = iv + b"\x00" * 0xC)
        if cipher.decrypt(f).find(b"BHFlag") != -1:
            print(key, iv)
"""
# b'\x03\x03\x03\x03\x03\x03\x03\x03' b'\xfa\xfa\xfa\xfa'

key = b'\x03\x03\x03\x03\x03\x03\x03\x03'
iv = b'\xfa\xfa\xfa\xfa'

cipher = AES.new(key + b"\x00" * 8, mode = AES.MODE_CBC, iv = iv + b"\x00" * 0xC)
print(cipher.decrypt(f))
