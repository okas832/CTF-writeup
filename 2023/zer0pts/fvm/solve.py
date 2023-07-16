import math
def bytes_to_m80(x):
    x = int.from_bytes(x, "little")
    sign = (x >> 79) & 1
    exp = (x >> 64) & (2 ** 16 - 1)
    frac = x & (2 ** 64 - 1)

    return frac * (2 ** (exp - 16383)) / (2 ** 63)


def find_near_a(k):
    mn = 99999999999999999999.0
    mi, mj = -1, -1
    for i in range(32, 127):
        for j in range(32, 127):
            dff = math.fabs((i * (((2 * math.pi * j) / 256) - math.sin((2 * math.pi * j) / 256))) - k)
            if dff < mn:
                mn, mi, mj = dff, i, j
    return mi, mj

def find_near_b(k):
    mn = 99999999999999999999.0
    mi, mj = -1, -1
    for i in range(32, 127):
        for j in range(32, 127):
            dff = math.fabs((i * ((math.cos((2 * math.pi * j) / 256)) + 1) * math.sin(((2 * math.pi * j) / 256))) - k)
            if dff < mn:
                mn, mi, mj = dff, i, j
    return mi, mj

def rev(v1, v2):
    mul = bytes_to_m80(v1)
    add = bytes_to_m80(v2)

    a = (add + math.sqrt((add ** 2) - (4 * mul))) / 2
    b = (add - math.sqrt((add ** 2) - (4 * mul))) / 2

    x1, x2 = find_near_a(a)
    x3, x4 = find_near_b(b)

    return bytes([x1, x2, x3, x4])

def rev2(v1, v2):
    mul = bytes_to_m80(v1)
    add = bytes_to_m80(v2)

    a = (add + math.sqrt((add ** 2) - (4 * mul))) / 2
    b = (add - math.sqrt((add ** 2) - (4 * mul))) / 2

    x1, x2 = find_near_a(b)
    x3, x4 = find_near_b(a)

    return bytes([x1, x2, x3, x4])


mul_lst = [[5, 63, 17, 244, 255, 41, 87, 129, 14, 64],
           [183, 115, 128, 225, 176, 114, 135, 242, 3, 64],
           [84, 39, 181, 182, 149, 82, 93, 205, 11, 64],
           [163, 134, 20, 5, 65, 140, 116, 229, 11, 64],
           [136, 146, 58, 224, 105, 63, 84, 146, 6, 64],
           [131, 234, 123, 151, 229, 76, 211, 234, 6, 64],           
           [25, 66, 108, 212, 202, 246, 242, 217, 9, 64],
           [254, 19, 151, 223, 205, 18, 126, 240, 10, 64]]
add_lst = [[94, 87, 243, 180, 163, 140, 127, 186, 7, 64],
           [63, 104, 163, 228, 4, 154, 59, 143, 7, 64],
           [40, 145, 154, 74, 162, 113, 55, 145, 7, 64],
           [188, 97, 237, 242, 233, 110, 193, 171, 6, 64],
           [15, 209, 190, 227, 57, 161, 150, 197, 5, 64],
           [135, 239, 176, 209, 92, 254, 134, 173, 4, 64],
           [239, 255, 218, 21, 19, 234, 174, 219, 6, 64],
           [28, 175, 207, 31, 150, 69, 65, 165, 6, 64]]
  
flag = b""
for mul, add in zip(mul_lst[:-1], add_lst[:-1]):
    flag += rev(mul, add)
flag += rev2(mul_lst[-1], add_lst[-1])
print(flag + b"}") # last block produce wrong answer
