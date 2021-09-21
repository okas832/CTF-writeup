import struct

u16 = lambda x: struct.unpack("<H", x)[0]

f = open("flag.jpg.enc", "rb").read()

f2 = open("flag.jpg", "wb")

l = len(f) // 2
k = -1
for i in range(0x100):
    p = u16(f[0:2])
    v4 = ((p << 3) & 0xFFFF) | ((p >> 13) & 0xFFFF)
    t = ((v4 & 0xE0) >> 5) | (((v4 >> 11) & 0x1F) << 3)
    t ^= 0xFF
    if t ^ i == 0xFF:
        k = i
        break

f2.write(bytes([0xFF]))
for i in range(1, l):
    p = u16(f[i * 2:i * 2 + 2])

    v4 = ((p << ((3 * i + 3) & 0xF)) & 0xFFFF) | ((p >> (16 - ((3 * i + 3) & 0xF))) & 0xFFFF)
    t = ((v4 & 0xE0) >> 5) | (((v4 >> 11) & 0x1F) << 3)
    t ^= 0xFF
    t ^= k
    f2.write(bytes([t]))

f2.close()

