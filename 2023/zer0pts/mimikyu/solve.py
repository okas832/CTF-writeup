
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def rev(e, c, n):
    n2 = n
    primes = []
        
    for i in range(2, 0x10000):
        if n2 % i == 0:
            primes.append(i)
            n2 //= i

    
    ts = []
    xs = []
    ds = []

    for i in range(len(primes)):
            ds.append(modinv(e, primes[i]-1))

    m = primes[0]

    for i in range(1, len(primes)):
            ts.append(modinv(m, primes[i]))
            m = m * primes[i]

    for i in range(len(primes)):
            xs.append(pow((c%primes[i]), ds[i], primes[i]))

    x = xs[0]
    m = primes[0]

    for i in range(1, len(primes)):
            x = x + m * ((xs[i] - x % primes[i]) * (ts[i-1] % primes[i]))
            m = m * primes[i]


    return (x % n).to_bytes(4, "little")


flag = b""

e = 0x000000000000f0d3
c = 0xFE4C025C5F4
n = 0x00002350f23a0dff
flag += rev(e, c, n)

e = 0x000000000000085f
c = 0x1B792FF17E8A
n = 0x000032d18e9d4d33
flag += rev(e, c, n)

e = 0x0000000000008e63
c = 0x183B156AB40
n = 0x000003866cd71f1b
flag += rev(e, c, n)

e = 0x0000000000008249
c = 0x0BEFFCF5E5DA
n = 0x000010ae9be3fc8f
flag += rev(e, c, n)

e = 0x000000000000c6a1
c = 0x297CF86E251
n = 0x000009d942eff67d
flag += rev(e, c, n)

e = 0x0000000000000c6d
c = 0xEB3EDC1D4B4
n = 0x00001de2e3aa8bb1
flag += rev(e, c, n)

e = 0x000000000000aef5
c = 0xFA10CE3A08
n = 0x0000103fc65841f3
flag += rev(e, c, n)

e = 0x000000000000d5df
c = 0x2BDD418672
n = 0x0000011a0970edc9
flag += rev(e, c, n)

e = 0x000000000000e68d
c = 0x5EBB5050EA46
n = 0x00005f8d20bddf39
flag += rev(e, c, n)

e = 0x000000000000f3fb
c = 0x5BF9B73CF86
n = 0x000045b14e11e0ed
flag += rev(e, c, n)

print(flag)
