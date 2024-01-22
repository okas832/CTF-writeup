ll = 0x1B75F5867FDA13B0
def x(s):
    v = (s << 0xd) ^ s
    v &= (1 << 64) - 1
    v = (v >> 7) ^ v
    s = (v << 0x11) ^ v
    s &= 0xFFFFFFFFFFFFFFFF
    return s

lst = [0xBDE671E813BA0EC4, 0xFE313878BFD3832A, 0xEFE4966FA7747A84, 0xAC6A45CFCC93F053]

flag = b""

ll = x(ll)
save_ll = lst[0] ^ ll
flag += (lst[0] ^ ll).to_bytes(8,  "little")
ll = save_ll

ll = x(ll)
flag += (lst[1] ^ ll).to_bytes(8,  "little")
ll = x(ll)
flag += (lst[2] ^ ll).to_bytes(8,  "little")
ll = x(ll)
flag += (lst[3] ^ ll).to_bytes(8,  "little")

print(flag)
