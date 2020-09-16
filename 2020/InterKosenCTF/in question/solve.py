a = [0xDB, 0xE2, 0xEB, 0xF7, 0xD6, 0xED, 0xEB, 0xC5, 0xE8, 0xA2, 0xAB, 0xEE, 0xD8, 0xC1, 0xAE, 0xB7, 0xC4, 0xC5, 0xF1, 0xB0, 0xAB, 0xC1, 0xD0, 0xBE, 0xE7, 0xBA, 0xD6, 0xCE, 0xEB, 0x9F, 0x00, 0x00]
b = [0 for _ in range(32)]

for i in range(30):
    i = 29 - i
    b[i] = (~i& 0xFF) ^ b[i + 1] ^ a[i]

print("".join(map(chr, b)))




