# Pickle Rick
Reversing, 220 points

## Description
```
I found a suspicious pickle file with a script...
,
Wait, who is Pickle Rick?
```
[Download](./pickle_rick.tar.gz)

## Analysis
Using pickletools, we can read the bytecode of it.  
Summarizing the bytecodes,
```
1. Print Big Pickle Rick and some interaction with user
...
17122: \x85 TUPLE1
17123: R    REDUCE
17124: c    GLOBAL     'builtins print'
17140: S    STRING     'Pickle Rick says:'
17161: \x85 TUPLE1
17162: R    REDUCE
17163: c    GLOBAL     'builtins print'
17179: c    GLOBAL     '__main__ rick_says'
17199: \x85 TUPLE1
17200: R    REDUCE
17201: c    GLOBAL     'builtins print'
17217: S    STRING     'The flag machine says:'

2. Build binary tree with tuple
17245: J    BININT     115
17250: \x85 TUPLE1
17251: J    BININT     99
17256: \x85 TUPLE1
17257: \x86 TUPLE2
17258: J    BININT     97
17263: \x85 TUPLE1
17264: J    BININT     162
17269: \x85 TUPLE1
17270: \x86 TUPLE2
...

3. Define two function in something_suspicious.py
19158: (    MARK
19159: J        BININT     2
19164: J        BININT     0
19169: J        BININT     0
19174: J        BININT     5
19179: J        BININT     6
19184: J        BININT     67
19189: B        BINBYTES   b'd\x01}\x02zB|\x00\\\x02}\x03}\x04|\x01d\x02\x16\x00|\x02k\x02r0|\x04}\x00|\x01d\x02\x1c\x00}\x01d\x03|\x02\x18\x00}\x02n\x14|\x03}\x00|\x01d\x02\x1c\x00}\x01d\x03|\x02\x18\x00}\x02W\x00q\x04\x01\x00\x01\x00\x01\x00|\x00d\x01\x19\x00\x06\x00Y\x00S\x000\x00q\x04d\x00S\x00'
...

1. Get input and do something and check input
19897: c    GLOBAL     'builtins print'
19913: c    GLOBAL     '__main__ amazing_function'
19940: (    MARK
19941: g        GET        1
19944: g        GET        0
19947: c        GLOBAL     '__main__ amazing_function'
19974: g        GET        2
19977: J        BININT     0
19982: \x86     TUPLE2
19983: R        REDUCE
19984: \x86     TUPLE2
19985: R        REDUCE
19986: g        GET        1
19989: g        GET        0
19992: c        GLOBAL     '__main__ amazing_function'
20019: g        GET        2
20022: J        BININT     1
...
```

Parse and build binary tree is easy. But need one more step because need to analyze functions in `something_suspicious.py`  
Pickle saves python function in raw data of `py_object`. We can make pyc file of it and use decompiler.  
But since it's too annoying, I chooses decompile this in my eyes and hands.  
The result is this
```python
# I know this is not same as original, maybe, but can guess with some debugging with amazing_function
def search(a, b):
    c = 0
    try:
        while True:
            a0, a1 = a
            if b % 2 == c:
                a = a1
                b /= 2
                c = 1 - c
            else:
                a = a0
                b /= 2
                c = 1 - c
    finally:
        return a[0]


def mix(a):
    ln = len(a)
    arr = []
    i = 0

    while i < ln:
        s, j = 0, 0
        while j < ln:
            s += (j + 1) *  a[i + j % ln]
            j += 1
        s %= 257
        if s < 256:
            raise
        arr.append(s)
        i += 1
    return arr
```

First `mix` is apply to input. It does matrix multiply and modular in 257.  
After that, it apply `search` to each byte.  
Finally, it compare with some array and it should be same.

# Solution
Making inverse function of `search` is easy, bruteforce and make a table or find path of binary tree. I choosed 2nd.  
For function `mix`, find and multiply modular inverse of matrix will do. sympy will do that.

See [solve.py](./solve.py)
