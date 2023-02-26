s = 777
lst = []

for i in range(0x10):
    lst.append(s & 0xF)
    if s & 1:
        s = 3 * s + 1
    else:
        s >>= 1

tbl = [0xF, 3, 0xA, 1, 4, 5, 0xC, 0xD, 9, 2, 6, 0xB, 8, 7, 0xE, 0]
ans = ""

for i in lst:
    i = tbl.index(i)
    ans += ("%X"%(i))[-1]

print("SECCON{" + ans + {"})
