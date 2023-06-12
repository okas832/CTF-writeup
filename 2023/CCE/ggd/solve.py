
f = open("dis1.txt", "rt").readlines()
s3 = []
for i in f[15::18]:
    s3.append(int(i.split('"')[5]))

f2 = open("dis2.txt", "rt").readlines()
xor = []
for i in f2[4::7]:
    xor.append(int(i.split('"')[5]))

def ADD(x, y):
    return (x + y) & 0xFF

def SUB(x, y):
    t = x - y
    if t < 0:
        t += 0x100
    return t

flag = list(b'cc')

for i in range(39):
    f1 = eval(f[18 * i + 11].split('"')[1])
    f2 = eval(f[18 * i + 13].split('"')[1])
    for j in range(0x100):
        if f2(f1(flag[i] ^ xor[i] ^ 77, flag[i + 1] ^ xor[i + 1] ^ 77), j) == s3[i]:
              flag.append(j ^ xor[i + 2] ^ 77)
              break

print(bytes(flag))
