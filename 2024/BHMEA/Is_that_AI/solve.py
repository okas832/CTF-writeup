p = open("./model.params", "rb").read()

import struct

jj = struct.unpack("<"+"i"*64, p[-(64 * 4 * 1):])
hh = struct.unpack("<"+"i"*64, p[-(64 * 4 * 2 + 8):-(64 * 4 * 1 + 8)])
aa = struct.unpack("<"+"i"*64, p[-(64 * 4 * 3 + 16):-(64 * 4 * 2 + 16)])

from z3 import *

flag = ""

for pp in range(64):

    j = jj[pp]
    h = hh[pp]
    a = aa[pp]

    s = Solver()
    ipt = Int('x')
    z = 0
    i = z * ipt + a - h
    c = ipt - (i + j)
    k = ipt * i * z
    s.add(k + c == 0)

    s.check()
    flag += chr(int(str(s.model()[ipt])))
print(flag)
