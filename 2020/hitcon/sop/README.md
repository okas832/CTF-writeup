

# SOP

Let me introduce a brand new concept - Syscall Oriented Programming!

[sop](./sop)

[sop_bytecode](./sop_bytecode)

15 Teams solved.

## Binary

This has small code.

```c
uint64_t getbit(uint64_t *v, uint8_t len)
{
    uint64_t ret = *v & ((1 << len) - 1);
    *v >>= len;
    return ret;
}
    
    
void fetch_inst(uint64_t inst, uint64_t *sysno, uint64_t *arg, uint64_t *reg)
{
    int i;
    int type;
	int imm_len;
    *sysno = getbit(&inst, 8);
    for(i = 0; i <= 5; i++)
    {
        type = getbit(&inst, 2);
        switch(type)
        {
            case 0:
                arg[i] = mem[getbit(&inst, 4)];
                break;
            case 1:
                arg[i] = &mem[getbit(&inst, 4)];
                break;
            case 2:
                imm_len = getbit(&inst, 5);
                arg[i] = getbit(&inst, imm_len + 1);
                break;
            default:
                return;
         }
    }
    return;
}

void run(uint64_t *code)
{
    uint64_t sysno;
    uint64_t arg[6];
    uint64_t reg[0x10];
    
    memset(reg, 0, 0x80);
    while ( code[reg[15]] )
    {
        fetch_inst(code[mem[15]], &sysno, arg, reg);
        syscall(sysno, arg[0], arg[1], arg[2], arg[3], arg[4], arg[5]);
        ++reg[15];
    }
    return;
}
```

Read 8 bytes from code, fetch and run syscall. It's easy to implement parser.

Let's take a look the sop_bytecode.

## sop_bytecode

Before looking the syscalls, I'll show you how to implement `mov` in syscall.

------

#### mov

```c
set_tid_address(0x217000);
prctl(PR_GET_TID_ADDRESS, &reg[0]);
```

This two syscall can move value. Set tid address to value with set_tid_address syscall, and use prctl's `PR_GET_TID_ADDRESS` option to get the value from the tid address to memory.
I'll write this as `reg[0] = 0x217000`

------

### 1. mmap
At first 3 syscalls, this mmap at 0x217000 with rwx. 

```c
reg[0] = 0x217000;
mmap (reg[0], 0x1, 0x7, 0x22, 0x0, 0x0)
```

### 2. sigaction

There are many `mov` and do `sigaction` 

```c
...
reg[9] = 0x217044
*(reg[9]) = 0xfb0c031
reg[7] = 0x217048
*(reg[7]) = 0xcccc050f
reg[0] = 0x217050
sigaction[SIGSYS, reg[0], 0x0, 0x8]
```

Setting up signal handler for SIGSYS.

```c
(struct sigaction *)0x217050
{
	.action = 0x217020;
	.sa_flags = 0x4000004; // SA_RESTORER | SA_SIGINFO
  	.sa_restorer = 0x217044;
  	.sa_mask = 0x0;
}
```

```asm
0x217020:
    movabs	rcx, 0x3f8495f5793a342c
    mov 	edx, dword ptr [rsi+4]
    mov 	word ptr [rcx], dx
    lea 	rcx, [rip - 0x15]
    inc 	qword ptr [rcx]
    inc 	qword ptr [rcx]
    ret

0x217044:
    xor		eax, eax
    mov		al, 0xf
    syscall              ; sigreturn
```

That `0x3f8495f5793a342c` has no meaning. It will change that value later.

### 3. seccomp

```c
prctl (PR_SET_NO_NEW_PRIVS, 0x1, 0x0, 0x0)
reg[13] = 0x217050
*(reg[13]) = 0x47
reg[12] = 0x217058
*(reg[12]) = 0x217060
...
reg[2] = 0x217290
*(reg[2]) = 0x6
reg[8] = 0x217294
*(reg[8]) = 0x7fff0000
prctl (PR_SET_SECCOMP, SECCOMP_MODE_FILTER, 0x217050]
```

After that, it set seccomp with custom filter.

```c
(struct prog*)0x217050
{
	.len = 0x47;
	.filter = 0x217060;
}
```

Using [author's seccomp tool](https://github.com/david942j/seccomp-tools) to disasm

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000000  A = sys_number
 0001: 0x35 0x0d 0x00 0x40000000  if (A >= 0x40000000) goto 0015
 0002: 0x15 0x0a 0x00 0x00000001  if (A == write) goto 0013
 0003: 0x15 0x20 0x00 0x00000068  if (A == getgid) goto 0036
 0004: 0x15 0x15 0x00 0x00000066  if (A == getuid) goto 0026
 0005: 0x15 0x28 0x00 0x000000ba  if (A == gettid) goto 0046
 0006: 0x15 0x0e 0x00 0x00000027  if (A == getpid) goto 0021
 0007: 0x15 0x17 0x00 0x0000006c  if (A == getegid) goto 0031
 0008: 0x15 0x07 0x00 0x0000006f  if (A == getpgrp) goto 0016
 0009: 0x15 0x29 0x00 0x0000006e  if (A == getppid) goto 0051
 0010: 0x15 0x1e 0x00 0x0000006b  if (A == geteuid) goto 0041
 0011: 0x15 0x2c 0x00 0x00000039  if (A == fork) goto 0056
 0012: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0013: 0x20 0x00 0x00 0x00000010  A = fd # write(fd, buf, count)
 0014: 0x15 0x00 0x37 0x00000000  if (A != 0x0) goto 0070
 0015: 0x06 0x00 0x00 0x00000000  return KILL
 0016: 0x20 0x00 0x00 0x00000018  A = args[1]
 0017: 0x07 0x00 0x00 0x00000000  X = A
 0018: 0x20 0x00 0x00 0x00000010  A = args[0]
 0019: 0x2c 0x00 0x00 0x00000000  A *= X      # getpgrp
 0020: 0x15 0x28 0x28 0x00000000  goto 0061
 0021: 0x20 0x00 0x00 0x00000018  A = args[1]
 0022: 0x07 0x00 0x00 0x00000000  X = A
 0023: 0x20 0x00 0x00 0x00000010  A = args[0]
 0024: 0x0c 0x00 0x00 0x00000000  A += X      # getpid
 0025: 0x15 0x23 0x23 0x00000000  goto 0061
 0026: 0x20 0x00 0x00 0x00000018  A = args[1]
 0027: 0x07 0x00 0x00 0x00000000  X = A
 0028: 0x20 0x00 0x00 0x00000010  A = args[0]
 0029: 0x7c 0x00 0x00 0x00000000  A >>= X     # getuid
 0030: 0x15 0x1e 0x1e 0x00000000  goto 0061
 0031: 0x20 0x00 0x00 0x00000018  A = args[1]
 0032: 0x07 0x00 0x00 0x00000000  X = A
 0033: 0x20 0x00 0x00 0x00000010  A = args[0]
 0034: 0x1c 0x00 0x00 0x00000000  A -= X      # getegid
 0035: 0x15 0x19 0x19 0x00000000  goto 0061
 0036: 0x20 0x00 0x00 0x00000018  A = args[1]
 0037: 0x07 0x00 0x00 0x00000000  X = A
 0038: 0x20 0x00 0x00 0x00000010  A = args[0]
 0039: 0x5c 0x00 0x00 0x00000000  A &= X      # getgid
 0040: 0x15 0x14 0x14 0x00000000  goto 0061
 0041: 0x20 0x00 0x00 0x00000018  A = args[1]
 0042: 0x07 0x00 0x00 0x00000000  X = A
 0043: 0x20 0x00 0x00 0x00000010  A = args[0]
 0044: 0xac 0x00 0x00 0x00000000  A ^= X      # geteuid
 0045: 0x15 0x0f 0x0f 0x00000000  goto 0061
 0046: 0x20 0x00 0x00 0x00000018  A = args[1]
 0047: 0x07 0x00 0x00 0x00000000  X = A
 0048: 0x20 0x00 0x00 0x00000010  A = args[0]
 0049: 0x4c 0x00 0x00 0x00000000  A |= X      # gettid
 0050: 0x15 0x0a 0x0a 0x00000000  goto 0061
 0051: 0x20 0x00 0x00 0x00000018  A = args[1]
 0052: 0x07 0x00 0x00 0x00000000  X = A
 0053: 0x20 0x00 0x00 0x00000010  A = args[0]
 0054: 0x6c 0x00 0x00 0x00000000  A <<= X     # getppid
 0055: 0x15 0x05 0x05 0x00000000  goto 0061
 0056: 0x20 0x00 0x00 0x00000018  A = args[1]
 0057: 0x07 0x00 0x00 0x00000000  X = A
 0058: 0x20 0x00 0x00 0x00000010  A = args[0]
 0059: 0x3c 0x00 0x00 0x00000000  A /= X      # fork
 0060: 0x15 0x00 0x00 0x00000000  /* no-op */
 0061: 0x02 0x00 0x00 0x00000000  mem[0] = A
 0062: 0x20 0x00 0x00 0x00000020  A = args[2]
 0063: 0x07 0x00 0x00 0x00000000  X = A
 0064: 0x60 0x00 0x00 0x00000000  A = mem[0]
 0065: 0x7c 0x00 0x00 0x00000000  A >>= X
 0066: 0x01 0x00 0x00 0x00030000  X = 0x30000 # SECCOMP_RET_TRAP
 0067: 0x54 0x00 0x00 0x0000ffff  A &= 0xffff
 0068: 0x4c 0x00 0x00 0x00000000  A |= X
 0069: 0x16 0x00 0x00 0x00000000  return A
 0070: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

There is ALU. If one of those(get*., fork) called, signal handler will called after that because of seccomp's return value.

With these, we can implement operations.

------

#### Arithmetic operations

```
*(uint64_t *)(0x217022) = &reg[12]
reg[0] = reg[12]
reg[1] = reg[3]
getpid(reg[0], reg[1], 0x0)
getpid(reg[0], reg[1], 0x10)
```

First line changes the SIGSYS handler function. In this case, it will change to

```asm
0x217020:
    movabs	rcx, &reg[12]
    mov 	edx, dword ptr [rsi+4]
    mov 	word ptr [rcx], dx
    lea 	rcx, [rip - 0x15]
    inc 	qword ptr [rcx]
    inc 	qword ptr [rcx]
    ret
```

Sigaction's `sa_flag` has `SA_SIGINFO`, so `rsi` holds `siginfo_t` address and in `[rsi+4]` there is errno, which is return value of seccomp filter. 

When the first getpid is called, seccomp filter will add `reg[0]`  and `reg[1]` and set errno to `(reg[0] + reg[1]) | SECCOMP_RET_TRAP` . So this raises SIGSYS and system calls handler for SIGSYS.

First 3 instruction in handler saves the result value to [rcx].(reg[12] right now)

And next 3 instruction add 2 to first instruction's second argument that changes `&reg[12]` to `&reg[12] + 2` for the next getpid.

Those syscalls can be summerize to

```
reg[12] = reg[12] + reg[3]
```

------

With these information, I wrote ["why does this work?" parser](./parser.py).

I'll pass analyzing the summarized code here. Only result.

```c
int f(unsigned int a, unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int x1, unsigned int x2)
{
    unsigned int k = e;
    int i;
    unsigned int i1, i2; // input
    i1 = input();
    i2 = input(); // actual program read whole input. this is just for understanding
    for (i = 0; i < 32; i++)
    {
        i1 = i1 + (((i2 << 0x4) + a) ^ ((i2 >> 0x5) + b) ^ (i2 + k));
        i2 = i2 + (((i1 << 0x4) + c) ^ ((i1 >> 0x5) + d) ^ (i1 + k));
        k += e;
    }
    if(x1 != i1 || x2 != i2)
        return 0;
    return 1;
}

int main()
{
    if(f(0x69a33fff, 0x468932dc, 0x2b0b575b, 0x1e8b51cc, 0x51fdd41a, 0x152ceed2, 0xd6046dc3)&&
	   f(0x32e57ab6, 0x7785df55, 0x688620f9, 0x8df954f3, 0x5c37a6db, 0x4a9d3ffd, 0xbb541082)&&
	   f(0xaca81571, 0x2c19574f, 0x1bd1fc38, 0x14220605, 0xb4f0b4fb, 0x632a4f78, 0xa9cb93d) &&
	   f(0x33f33fe0, 0xf9de7e36, 0xe9ab109d, 0x8d4f04b2, 0xd3c45f8c, 0x58aae351, 0x92012a14))
    {
        // correct!
    }
    // fail...
    return 0;
}
```

We can find the input by just calculate back.

And this is a solution.

```c
#include<stdio.h>

void f(unsigned int a, unsigned int b, unsigned int c, unsigned int d, unsigned int e, unsigned int x1, unsigned int x2)
{
    unsigned int k = e * 0x20;
    int i;
    for (i = 0; i < 32; i++)
    {
        x2 = x2 - (((x1 << 0x4) + c) ^ ((x1 >> 0x5) + d) ^ (x1 + k));
        x1 = x1 - (((x2 << 0x4) + a) ^ ((x2 >> 0x5) + b) ^ (x2 + k));
        k -= e;
    }
    printf("%c%c%c%c%c%c%c%c",  *(((char*)&x1) + 0),
		                *(((char*)&x1) + 1),
				*(((char*)&x1) + 2),
				*(((char*)&x1) + 3),
				*(((char*)&x2) + 0),
				*(((char*)&x2) + 1),
				*(((char*)&x2) + 2),
				*(((char*)&x2) + 3)
	  );
}

int main()
{
    f(0x69a33fff, 0x468932dc, 0x2b0b575b, 0x1e8b51cc, 0x51fdd41a, 0x152ceed2, 0xd6046dc3);
    f(0x32e57ab6, 0x7785df55, 0x688620f9, 0x8df954f3, 0x5c37a6db, 0x4a9d3ffd, 0xbb541082);
    f(0xaca81571, 0x2c19574f, 0x1bd1fc38, 0x14220605, 0xb4f0b4fb, 0x632a4f78, 0xa9cb93d);
    f(0x33f33fe0, 0xf9de7e36, 0xe9ab109d, 0x8d4f04b2, 0xd3c45f8c, 0x58aae351, 0x92012a14);
    return 0;
}
```

## Comments

Great challenge. I learned evil techniques to make evil binary. But can we make ALU without signal handler or seccomp thing? I'll try for it.
