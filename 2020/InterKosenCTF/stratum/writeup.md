# startum

### Binary

There are some SIMD instruction here. With short time of analyzing binary and give some inputs with little changes, we can get the encryption logic.

```python
ipt : list with bytes(16) element
f : output file 
for i in range(?):
	a = ipt[i]; b = ipt[i+1]
	out1 = _mm_shuffle_epi8("asdfghjklzxcvbnm", a);
	for j in range(16):
		out2[j] = b[j] ^ (lzcnt16(a[j] << 8) | (popcnt16(a[j]) * 16))

    f.write(out1)
    f.write(out2)
	
```

We can know that output is related on two 16 bytes in a row.

### Solution

It's easy to reverse `out1` to `a` elements' low 4 bit. But it is not possible to recover a elements' high 4 bit and b from out2 and a elements' low 4 bit. But there will be some chain relation between 16 bytes chunks. So I make a script that prints all possible pairs    from the encrypted file.

```python
import string

a = "asdfghjklzxcvbnm"
f = open("./flag.enc", "rb")

t = string.ascii_letters + string.digits + "{-_?!}"

tb = {}

def lzcnt16(x):
    x = x & 0xFFFF
    cnt = 16
    while x:
        x >>= 1
        cnt -= 1
    return cnt

def popcnt16(x):
    x = x & 0xFFFF
    cnt = 0
    while x:
        if x & 1:
            cnt += 1
        x >>= 1
    return cnt

def shuffle(x):
    x = x & 0xF
    return a[x]

for c1 in t:
    for c2 in t:
        k = (shuffle(ord(c1)), ord(c2) ^ (lzcnt16(ord(c1) << 8) | (popcnt16(ord(c1)) * 16)))
        if tb.get(k):
            tb[k].append((c1, c2))
        else:
            tb[k] = [(c1, c2)]

for i in range(4):
    info1 = f.read(16)
    info2 = f.read(16)

    for i1, i2 in zip(info1, info2):
        print(i1, i2, tb[(i1, ord(i2))])
    print("")
        
"""
KosenCTF{h4v3_fu
n_w17h_7h3_ugly_
bu7_u53ful_SIMD_
1n57ruc710n5}
"""
```

For example, we know the input starts with `KosenCTF{`. So we can get `n_w17h_7h`, `bu7_u53fu` and`1n57ruc71` by checking the possible inputs. Likewise, we can retrieve the rest of the part.