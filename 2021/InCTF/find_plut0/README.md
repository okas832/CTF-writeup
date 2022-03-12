# find_plut0
### Binary

Flag checker with simple operations.

```c
scanf("%s", ipt);
if ( strlen(ipt) != 30 )
  Fail();
array[0] = ipt[0] - 50 + ipt[1];
array[1] = ipt[1] - 100 + ipt[2];
array[2] = 4 * ipt[2];
array[3] = ipt[3] ^ 0x46;
array[4] = 36 - (ipt[3] - ipt[4]);
array[6] = ipt[6] * ipt[5] + 99;
array[7] = (char)(ipt[6] ^ ipt[7]);
array[8] = (ipt[7] + 45) ^ ipt[8];
array[9] = (ipt[9] & 0x37) - 3;
array[11] = ipt[11] - 38;
array[12] = 4 * ((char)(ipt[12] ^ ipt[6]) + 4);
array[5] = (ipt[21] - ipt[4]) ^ 0x30;
array[13] = ipt[13] - ipt[14] - 1;
array[10] = ipt[17] - ipt[16] + 82;
array[16] = 6 * (char)(ipt[18] ^ ipt[19]) + 54;
array[17] = ipt[21] + 49 + (ipt[20] ^ 0x73);
array[14] = ipt[22];
array[18] = ipt[23] ^ 0x42;
array[15] = ipt[26] + 5;
array[19] = ipt[25] - ipt[26] / 2 - 55;
array[20] = 4 * ipt[27] - (ipt[28] + 128);
array[21] = ipt[29] - 32;

s1[0] = (*array ^ 2) - 31;
s1[1] = ((array[1] % 2) ^ *array) - 29;
s1[2] = (4 * array[1]) ^ 0x97;
s1[3] = array[2] ^ 0xA0;
s1[4] = (array[3] ^ 0x4D) + 7;
s1[5] = 4 * array[5] - 1;
s1[3] = array[4] + 116;
s1[6] = array[6] + 21;
s1[7] = array[7] - 20;
s1[8] = array[8] ^ 0x63;
s1[9] = (array[10] ^ 3) - array[8] + 54;
s1[10] = array[9] ^ 0x42;
s1[11] = array[11] + 51;
s1[11] = array[12] ^ 0xB3;
s1[12] = (array[13] + 18) ^ 0x1A;
s1[13] = array[14] - 7;
s1[14] = array[15] - 37;
s1[15] = array[17] ^ 0xE5;
s1[16] = (array[18] & 0x36) + 53;
s1[14] = array[19] ^ 0x34;
s1[17] = array[20] ^ 0xFD;
s1[18] = ((int)array[20] >> array[21]) ^ 0x1C;

if(!strcmp(s1, "inctf{U_Sur3_m4Te?}"))
	Win();
Fail();
```

### Solution

Z3-solver will do.

```python
from z3 import *

ipt = [BitVec("ipt_%d"%i, 9) for i in range(30)]
array = [0 for i in range(22)]

s = Solver()

for i in range(30):
    s.add(ipt[i] > 32)
    s.add(ipt[i] < 127)

array[0] = ipt[0] - 50 + ipt[1]
array[1] = ipt[1] - 100 + ipt[2]
array[2] = 4 * ipt[2]
array[3] = ipt[3] ^ 0x46
array[4] = 36 - (ipt[3] - ipt[4])
array[6] = ipt[6] * ipt[5] + 99
array[7] = (ipt[6] ^ ipt[7])
array[8] = (ipt[7] + 45) ^ ipt[8]
array[9] = (ipt[9] & 0x37) - 3
array[11] = ipt[11] - 38
array[12] = 4 * ((ipt[12] ^ ipt[6]) + 4)
array[5] = (ipt[21] - ipt[4]) ^ 0x30
array[13] = ipt[13] - ipt[14] - 1
array[10] = ipt[17] - ipt[16] + 82
array[16] = 6 * (ipt[18] ^ ipt[19]) + 54
array[17] = ipt[21] + 49 + (ipt[20] ^ 0x73)
array[14] = ipt[22]
array[18] = ipt[23] ^ 0x42
array[15] = ipt[26] + 5
array[19] = ipt[25] - ipt[26] / 2 - 55
array[20] = 4 * ipt[27] - (ipt[28] + 128)
array[21] = ipt[29] - 32

s1 = list(b"inctf{U_Sur3_m4Te?}")

s.add(s1[0]  == (array[0] ^ 2) - 31)
s.add(s1[1]  == ((array[1] % 2) ^ array[0]) - 29)
s.add(s1[2]  == (4 * array[1]) ^ 0x97)
s.add(s1[3]  == array[2] ^ 0xA0)
s.add(s1[4]  == (array[3] ^ 0x4D) + 7)
s.add(s1[5]  == 4 * array[5] - 1)
s.add(s1[3]  == array[4] + 116)
s.add(s1[6]  == array[6] + 21)
s.add(s1[7]  == array[7] - 20)
s.add(s1[8]  == array[8] ^ 0x63)
s.add(s1[9]  == (array[10] ^ 3) - array[8] + 54)
s.add(s1[10] == array[9] ^ 0x42)
s.add(s1[11] == array[11] + 51)
s.add(s1[11] == array[12] ^ 0xB3)
s.add(s1[12] == (array[13] + 18) ^ 0x1A)
s.add(s1[13] == array[14] - 7)
s.add(s1[14] == array[15] - 37)
s.add(s1[15] == array[17] ^ 0xE5)
s.add(s1[16] == (array[18] & 0x36) + 53)
s.add(s1[14] == array[19] ^ 0x34)
s.add(s1[17] == array[20] ^ 0xFD)
s.add(s1[18] == (array[20] >> array[21]) ^ 0x1C)

s.check()

ans = ""
m = s.model()
for i in ipt:
    ans += chr(m[i].as_long())
print(ans)
```

But gives strange output.

```
Pl5T0!=NK3@&!`,@)C@@R_t2!aT\.!
```

I checked and found that other valid input exists. 

I asked admin about this. And they closed the challenge and gives input validation server when reopen.

