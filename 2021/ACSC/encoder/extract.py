from pwn import *

r = process(["gdb", "./encoder2"])

r.recvuntil("pwndbg> ")
r.sendline("b *0x555555554000 + 0x1400")

r.recvuntil("pwndbg> ")
r.sendline("r ./asdf")

arr = []

for i in range(0xFF):

    r.recvuntil("pwndbg> ")
    r.sendline("c")

    r.recvuntil("pwndbg> ")
    r.sendline("x/bx $rbp-0x42")

    arr.append(int(r.recvline().split(b"\t")[1], 16))

print(arr)

r.close()
