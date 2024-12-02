from PIL import Image

tbl = []

# parse image
for i in range(97):
    im = Image.open('%d.png'%(i))
    rgb_im = im.convert('RGB')

    y = 450
    x = 50

    blue = (135, 206, 235)
    white = (255, 255, 255)

    arr = []

    for i in range(23):
        if rgb_im.getpixel((x, y)) == blue:
            ty = y
            while True:
                if rgb_im.getpixel((x, ty)) == white:
                    break
                ty -= 1
            arr.append((416 - ty) // 55)

        while rgb_im.getpixel((x, y)) == blue:
            x += 1
        while rgb_im.getpixel((x, y)) == white:
            x += 1

    tbl.append(arr)

lll = [
    [0, 4, 0, 1, 0, 0, 0, 7, 0, 3, 7, 0, 0, 7, 0, 0, 5, 0, 0, 4, 0, 1, 0],
    [0, 3, 0, 1, 4, 0, 3, 0, 0, 2, 0, 0, 0, 2, 0, 0, 5, 0, 0, 7, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 7, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1, 1, 0, 1, 0],
    [0, 4, 0, 0, 7, 0, 2, 4, 0, 2, 7, 0, 0, 2, 7, 0, 1, 0, 1, 2, 0, 1, 0],
    [0, 6, 0, 1, 3, 0, 1, 7, 0, 0, 7, 0, 0, 6, 7, 0, 5, 0, 0, 3, 0, 1, 0],
    [0, 4, 0, 0, 4, 0, 3, 7, 0, 2, 7, 0, 0, 1, 0, 0, 4, 7, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 2, 0, 0, 3, 0, 3, 4, 7, 0, 5, 7, 0, 6, 7, 1, 5, 0, 1, 0]]

c = {}

def f(x, y):
    return [i[0] ^ i[1] for i in zip(x, y)]

for i in range(32, 128):
    val = [0 for i in range(23)]

    if i & 1:
        val = f(val, lll[0])
    if i & 2:
        val = f(val, lll[1])
    if i & 4:
        val = f(val, lll[2])
    if i & 8:
        val = f(val, lll[3])
    if i & 16:
        val = f(val, lll[4])
    if i & 32:
        val = f(val, lll[5])
    if i & 64:
        val = f(val, lll[6])
    else:
        val = f(val, [0, 3, 0, 0, 7, 0, 1, 7, 0, 2, 0, 7, 0, 5, 0, 0, 0, 0, 1, 0, 0, 1, 0])

    c[tuple(val)] = chr(i)

flag = ""
for i in tbl:
    try:
        flag += c[tuple(i)]
    except:
        print(tuple(i))
        flag += "?"
print(flag)
