# encoder
Reversing, 270 Points

# Description
recover flag file
[Download](./encoder.tar.gz)

# Analysis
There are some anti-disassembler bytecode in binary, but not many. Patch them to nop will do.
Self-modifying binary. When cpu meets `ud2` instruction, signal handler decode the instructions and execute it.

# Solution

Format of encoded instruction is
```
\x0f \x0B   ud2
\xXX        encoded data length
...         encoded data(len == 0xXX)
```

It does bit swapping and substract a value comes from generator.
I didn't implement that value generator, instead I extract the value from binary with gdb.
Just choose any `ud2` instruction in binary, change length to 0xFF and extract the values while it's decoding

```python
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
```

After that, I make IDA script to decode the encoded bytecodes.
```python
import idc
import idaapi

start_addr = 0x194C

arr = [33, 255, 255, 255, 255, 187, 51, 35, 190, 68, 156, 4, 157, 34, 210, 82, 74, 249, 161, 98, 57, 232, 230, 112, 215, 37, 253, 102, 87, 244, 242, 124, 219, 42, 209, 114, 228, 17, 222, 161, 57, 239, 231, 145, 80, 190, 36, 254, 62, 54, 52, 29, 149, 44, 123, 132, 188, 122, 187, 36, 49, 248, 129, 226, 216, 161, 23, 49, 255, 252, 135, 254, 220, 197, 51, 191, 4, 152, 236, 22, 44, 89, 185, 5, 97, 54, 250, 26, 208, 134, 22, 50, 238, 76, 142, 79, 5, 227, 50, 193, 42, 224, 170, 99, 162, 63, 54, 205, 62, 228, 198, 159, 166, 92, 91, 113, 203, 248, 202, 211, 178, 105, 239, 134, 40, 21, 55, 225, 208, 150, 60, 11, 189, 91, 187, 231, 236, 170, 80, 183, 201, 113, 72, 4, 137, 31, 87, 197, 229, 141, 156, 105, 31, 38, 116, 82, 114, 26, 98, 5, 124, 43, 11, 6, 174, 46, 119, 18, 72, 223, 16, 243, 186, 53, 195, 46, 95, 3, 173, 71, 214, 100, 95, 51, 235, 23, 185, 139, 234, 122, 227, 79, 255, 28, 61, 208, 2, 89, 136, 197, 59, 163, 90, 84, 46, 110, 158, 10, 15, 184, 159, 88, 212, 154, 195, 39, 45, 13, 19, 230, 242, 166, 223, 43, 193, 41, 232, 3, 176, 242, 235, 66, 93, 46, 61, 71, 205, 41, 191, 70, 155, 50, 202, 124, 81, 182, 203, 91, 63, 54, 214, 168, 166, 20, 89]

it = start_addr
while it <= 0x1C47:
    if 0xf == idaapi.get_byte(it) and 0xb == idaapi.get_byte(it + 1):
        l = idaapi.get_byte(it+2)
        idaapi.patch_byte(it, 0x90)
        idaapi.patch_byte(it+1, 0x90)
        idaapi.patch_byte(it+2, 0x90)
        it = it + 3
        for i in range(l):
            c = idaapi.get_byte(it + i)
            c = ((c & 0x8) >> 3) | ((c & 0x7) << 1) | ((c & 0x80) >> 3) | ((c & 0x70) << 1)
            c -= arr[i]
            if c < 0:
                c += 0x100
            idaapi.patch_byte(it + i, c)
        it += l
    else:
        it += 1
```

Finally, I can get `main` function's decompiled code.
```c
int main(int argc, char **argv)
{
  unsigned __int16 v4; // [rsp+1Ah] [rbp-56h]
  int i; // [rsp+24h] [rbp-4Ch]
  unsigned __int8 v6; // [rsp+2Bh] [rbp-45h]
  FILE *v7; // [rsp+40h] [rbp-30h]
  _WORD *ptr; // [rsp+48h] [rbp-28h]
  char *s; // [rsp+50h] [rbp-20h]
  int v10; // [rsp+5Ch] [rbp-14h]
  FILE *stream; // [rsp+60h] [rbp-10h]

  mprotect((sub_191B & 0xFFFFFFFFFFFFF000LL), 0x4000uLL, 7);
  if ( a1 > 1 )
  {
    stream = fopen(a2[1], "rb");
    if ( stream )
    {
      fseek(stream, 0LL, 2);
      v10 = ftell(stream);
      fseek(stream, 0LL, 0);

      s = malloc(v10);
      memset(s, 0, v10);
      fread(s, v10, 1uLL, stream);
      fclose(stream);
      ptr = malloc(2LL * v10);
      v6 = dword_204040;
      for ( i = 0; v10 > i; ++i )
      {
        v4 = (32 * (~(v6 ^ s[i]) & 7)) | ((~((v6 ^ s[i]) >> 3) & 0x1F) << 11);
        ptr[i] = (v4 >> ((3 * (i + 1)) & 0xF)) | (v4 << (16 - ((3 * (i + 1)) & 0xF)));
      }
      strcat(filename, a2[1]);
      strcat(filename, ".enc");
      v7 = fopen(filename, "wb");
      fwrite(ptr, 2LL * v10, 1uLL, v7);
      fclose(v7);
      free(ptr);
      return 0LL;
    }
    else
    {
      puts("open error");
      return 0LL;
    }
  }
  else
  {
    printf("[*] Usage : %s [file]\n", *a2);
    return 0LL;
  }
}
```

There is a random value `v6`. We don't know which value was set. But we know the flag file is in jpg, so magic value in header will solve this problem.

See [solve.py](./solve.py)

## Flag
<img src="flag.jpg" alt="Flag" style="zoom:50%;" /> 
