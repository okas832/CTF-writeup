# decompile me

Reverse engineering is getting easier thanks to IDA/Ghidra decompiler!

[chall](./chall)

124 Teams solved.

## Solution

When you do reversing, do not fully rely on decompiler.

`RC4_setkey` calling convention is not normal; r12, r13 not rdi, rsi. Also on `memcpy`.

## Flag

`zer0pts{d0n'7_4lw4y5_7ru57_d3c0mp1l3r}`