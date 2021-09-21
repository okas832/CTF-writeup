import struct
from z3 import *

f = open("Tnzr.exe", "rb").read()

lst = struct.unpack("<" + "I" * 7875, f[0x3c30 : 0xB73C])
lst2 = struct.unpack("<" + "I" * 7875, f[0xD650 : 0x1515C])
off = 780 // 4

iptoff = 13

v1 = 9669

for i in range(0, 7875, 225):
    x = [Int("x%d"%i) for i in range(225)]

    s = Solver()

    for j in range(225):
        s.add(x[j] >= 0)
        s.add(x[j] <= 2)

    for j in range(15): # v6
        for k in range(15):  #  v9
            t = 0
            for l in range(15):
                 t += x[15 * j + l] * lst[i + 15 * l+ k]
            s.add(t == lst2[i + 15 * j + k])


    print(s.check())
    m = s.model()
    ans = ""
    for i in range(15):
        for j in range(15):
            ans += "0" if str(m[x[i * 15 + j]]) != "0" else " "
        ans += "\n"
    print(ans)

