import string

a = "asdfghjklzxcvbnm"

f = open("./flag.enc", "rb")

t = string.ascii_letters + string.digits + "{-_?!}"

tb = {}

def lzcnt16(x):
    x = x & 0xFFFF
    cnt = 16
    while x:
        x >>= 1
        cnt -= 1
    return cnt

def popcnt16(x):
    x = x & 0xFFFF
    cnt = 0
    while x:
        if x & 1:
            cnt += 1
        x >>= 1
    return cnt

def shuffle(x):
    x = x & 0xF
    return a[x]

for c1 in t:
    for c2 in t:
        k = (shuffle(ord(c1)), ord(c2) ^ (lzcnt16(ord(c1) << 8) | (popcnt16(ord(c1)) * 16)))
        if tb.get(k):
            tb[k].append((c1, c2))
        else:
            tb[k] = [(c1, c2)]

for i in range(4):
    info1 = f.read(16)
    info2 = f.read(16)

    for i1, i2 in zip(info1, info2):
        print(i1, i2, tb[(i1, ord(i2))])
    print("")
        
"""
KosenCTF{h4v3_fu
n_w17h_7h3_ugly_
bu7_u53ful_SIMD_
1n57ruc710n5}
"""
