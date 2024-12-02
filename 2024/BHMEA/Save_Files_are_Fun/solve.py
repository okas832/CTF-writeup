from PIL import Image

f = open("map.wbox", "rb").read()
import zlib
f2 = zlib.decompress(f)
import json
jj = json.loads(f2)

im = Image.new(mode="RGB", size=(1000, 1000))

color = {0:(0,0,0), 1:(255, 0, 0), 2:(255, 255, 255)}

for i in range(320):
    j = 0
    for ot, oc in zip(jj["tileArray"][i], jj["tileAmounts"][i]):
        print(ot, oc)
        for k in range(oc):
            im.putpixel((i, j), color[ot])
            j += 1

im.show()
