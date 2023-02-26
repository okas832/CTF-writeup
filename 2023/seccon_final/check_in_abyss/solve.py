arr = [i for i in range(0x100)]

v11 = 0
v12 = 0xBA77C1

for i in range(0x100):
    v11 = (v11 + v12 + arr[i]) & 0xFF
    arr[i], arr[v11] = arr[v11], arr[i]
    v12 = (v12 * v12) & 0xFF

enc = [0x08, 0x27, 0x91, 0x13, 0x80, 0x1A, 0x66, 0x44, 0xAC, 0x8C,
  0x07, 0xAC, 0x15, 0xC4, 0xB2, 0x5D, 0xDF, 0xE6, 0x4B, 0xE6,
  0x74, 0x40, 0x95, 0x57, 0xBC, 0x14, 0xFA, 0xD8, 0x56, 0x58,
  0x7E, 0x63, 0x9F, 0xE4, 0x8F, 0xA1, 0x79, 0x38, 0x97, 0x6E,
  0xAD, 0x4A, 0x10, 0x8C, 0xF7, 0x22, 0x8A, 0x33, 0x00, 0x1F,
  0x1D, 0xF2, 0x04, 0xB7, 0x6B, 0x00, 0x68, 0x61, 0x6E, 0x64,
  0x6C, 0x65, 0x5F, 0x73]

flag = []

for j in range(8):
    key = []
    v16 = 0
    for i in range(8):
        v23 = arr[i]
        v16 = (arr[i] + v16) & 0xFF
        arr[i] = arr[v16]
        arr[v16] = v23

        key.append(arr[(arr[i] + v23) & 0xFF])
    key = key[::-1]

    for i in range(8):
        enc[8 * j + i] ^= key[i % len(key)]

print(bytes(enc))


