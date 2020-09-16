# in question

### Binary

Symbol in binary screwed up. We need to find main first.

<img src=".\img\symbol.png" width="200">

```assembly
.text:00000000004001A5                 public ??????_6
.text:00000000004001A5 ??????_6        proc near     
.text:00000000004001A5                 xor     rbp, rbp
.text:00000000004001A8                 mov     rdi, rsp
.text:00000000004001AB                 lea     rsi, cs:0
.text:00000000004001B2                 and     rsp, 0FFFFFFFFFFFFFFF0h
.text:00000000004001B6                 call    $+5
.text:00000000004001B6 ??????_6        endp ; sp-analysis failed
.text:00000000004001B6
.text:00000000004001BB
.text:00000000004001BB ; =============== S U B R O U T I N E ================
.text:00000000004001BB
.text:00000000004001BB
.text:00000000004001BB                 public ????????_5
.text:00000000004001BB ????????_5      proc near
.text:00000000004001BB                 lea     rdx, [rdi+8]
.text:00000000004001BF                 mov     rsi, [rdi]
.text:00000000004001C2                 mov     r8, offset _term_proc
.text:00000000004001C9                 mov     rcx, offset _init_proc
.text:00000000004001D0                 mov     rdi, offset ????_0
.text:00000000004001D7                 xor     r9d, r9d
.text:00000000004001DA                 jmp     ?????????????????_2
.text:00000000004001DA ????????_5      endp
```

0x4001A5; This is binary entry, and looks like gcc's `_start`. Because of the format of it, `????_0` is main.

```asm
.text:0000000000400152                 public ????_0
.text:0000000000400152 ????_0          proc near               ; DATA XREF: ????????_5+15↓o
.text:0000000000400152 ; __unwind {
.text:0000000000400152                 dec     edi
.text:0000000000400154                 push    rbx
.text:0000000000400155                 jg      short loc_40016F
.text:0000000000400157                 mov     rsi, [rsi]
.text:000000000040015A                 lea     rdi, aUsageSFlag ; "Usage: %s <FLAG>\n"
.text:0000000000400161                 xor     eax, eax
.text:0000000000400163                 mov     ebx, 1
.text:0000000000400168                 call    ??????_4
.text:000000000040016D                 jmp     short loc_4001A1
.text:000000000040016F ; ---------------------------------------------------------------------------
.text:000000000040016F
.text:000000000040016F loc_40016F:                             ; CODE XREF: ????_0+3↑j
.text:000000000040016F                 mov     rdi, [rsi+8]    ; a1
.text:0000000000400173                 lea     rsi, ??????_11  ; a2
.text:000000000040017A                 call    ?????
.text:000000000040017F                 test    eax, eax
.text:0000000000400181                 mov     ebx, eax
.text:0000000000400183                 jnz     short loc_400193
.text:0000000000400185                 lea     rdi, aCorrect   ; "Correct!"
.text:000000000040018C                 call    ????
.text:0000000000400191                 jmp     short loc_4001A1
.text:0000000000400193 ; ---------------------------------------------------------------------------
.text:0000000000400193
.text:0000000000400193 loc_400193:                             ; CODE XREF: ????_0+31↑j
.text:0000000000400193                 lea     rdi, aWrong     ; "Wrong..."
.text:000000000040019A                 xor     ebx, ebx
.text:000000000040019C                 call    ????
.text:00000000004001A1
.text:00000000004001A1 loc_4001A1:                             ; CODE XREF: ????_0+1B↑j
.text:00000000004001A1                                         ; ????_0+3F↑j
.text:00000000004001A1                 mov     eax, ebx
.text:00000000004001A3                 pop     rbx
.text:00000000004001A4                 retn
.text:00000000004001A4 ; } // starts at 400152
.text:00000000004001A4 ????_0          endp
```

Function `?????`, called by call instruction at `0x40017A`, looks important. It's the main cause of choosing the path to printing "Correct!" or "Wrong...".(Function `????` mentioned in `0x400185` and `0x40019c` is `puts` I think) 

#### Function ?????

If you are using IDA, decompiler will not show the decompiled code nice. But we can just reference it.

```c
__int64 __fastcall _____(const char *a1, const char *a2)
{
  __int64 v2; // rax
  int v3; // edi
  int v4; // edx
  int v5; // edi
  int v7; // [rsp-18h] [rbp-18h]
  __int64 v8; // [rsp-10h] [rbp-10h]
  __int64 v9; // [rsp-8h] [rbp-8h]

  strlen(a1);
  v2 = 0LL;
  while ( v2 < v7 )
  {
    v3 = v2;
    LOBYTE(v3) = ~v2;
    v4 = v3 ^ (*(v9 + v2 + 1) ^ *(v9 + v2));
    v5 = *(v8 + v2++);
    if ( v4 != v5 )
      return 1LL;
  }
  return 0LL;
}
```

Let's look at assembly instead.

```assembly
.text:00000000004002BA                 or      rcx, 0FFFFFFFFFFFFFFFFh
.text:00000000004002BE                 xor     eax, eax
.text:00000000004002C0                 mov     r8, rdi
.text:00000000004002C3                 repne scasb    # strlen thing
.text:00000000004002C5                 not     rcx
.text:00000000004002C8                 dec     ecx
.text:00000000004002CA                 push    r8
.text:00000000004002CC                 push    rsi
.text:00000000004002CD                 push    rcx
.text:00000000004002CE                 push    rax
.text:00000000004002CF                 xor     eax, eax
.text:00000000004002D1                 jz      short ??????_14
.text:00000000004002D3                 add     rsp, 309h
.text:00000000004002DA
.text:00000000004002DA ??????_14:                              ; CODE XREF: ?????+17↑j
.text:00000000004002DA                 pop     rax
.text:00000000004002DB                 pop     rcx
.text:00000000004002DC                 pop     rsi
.text:00000000004002DD                 pop     r8
.text:00000000004002DF                 xor     eax, eax
.text:00000000004002E1
.text:00000000004002E1 loc_4002E1:                             ; CODE XREF: ?????+48↓j
.text:00000000004002E1                 cmp     eax, ecx
.text:00000000004002E3                 jge     short loc_40030A
.text:00000000004002E5                 mov     dl, [r8+rax]
.text:00000000004002E9                 xor     dl, [r8+rax+1]
.text:00000000004002EE                 mov     edi, eax
.text:00000000004002F0                 xor     dil, 0FFh
.text:00000000004002F4                 movzx   edx, dl
.text:00000000004002F7                 xor     edx, edi
.text:00000000004002F9                 movzx   edi, byte ptr [rsi+rax]
.text:00000000004002FD                 inc     rax
.text:0000000000400300                 cmp     edx, edi
.text:0000000000400302                 jz      short loc_4002E1
.text:0000000000400304                 mov     eax, 1
.text:0000000000400309                 retn
```

`ecx` holds the strlen value. So `v7` is `strlen(a1)` value.

`v8` is `rsi`, the pointer referencing array `??????_11`.

`v9` is `r8`, and `r8`'s value comes from `rdi`(instruction at 0x4002C0). And it's `argv[1]`.

After fixing the code,

```c
__int64 __fastcall _____(const char *a1, const char *a2)
{
  ...// variable declared here

  v7 = strlen(a1);
  v2 = 0LL;
  while ( v2 < v7 )
  {
    v3 = ~v2;
    v4 = v3 ^ a1[v2 + 1] ^ a1[v2];
    v5 = a2[v2++];
    if ( v4 != v5 )
      return 1LL;
  }
  return 0LL;
}
```

### Solution

We know `a1[strlen(a1)] `is 0. We can compute a1 backward.

```python
a1 = [0 for _ in range(32)]
a2 = [0xDB, 0xE2, 0xEB, 0xF7, 0xD6, 0xED, 0xEB, 0xC5, 0xE8, 0xA2, 0xAB, 0xEE, 0xD8, 0xC1, 0xAE, 0xB7, 0xC4, 0xC5, 0xF1, 0xB0, 0xAB, 0xC1, 0xD0, 0xBE, 0xE7, 0xBA, 0xD6, 0xCE, 0xEB, 0x9F, 0x00, 0x00]

for i in range(30):
    i = 29 - i
    a1[i] = (~i& 0xFF) ^ a1[i + 1] ^ a2[i]

print("".join(map(chr, b)))
```

