from pwn import *

e = ELF("./breakout")

flag = []

for i in range(47):
    tbl = []
    for j in range(256):
        tbl.append(u64(e.read(e.address + 0x4040 + 256 * 8 * i + 8 * j , 8)))
    flag.append(tbl.index(min(tbl)))

print(b"BHFlagY{" + bytes(flag)[::-1] + b"}")

