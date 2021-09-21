# Tnzr
Reversing, 360 points

## Description
A flag checker! Mark the "Flag checker" on your CTF Reversing BINGO !!
[Download](./tnzr.tar.gz)

## Analyze
We can move cursor with arrow key, and set some marker on cursor with space.
When `c` is clicked, it do something and prints wrong.

There is a function that prints "Wrong" or "NICE" depend on one global byte data.
By finding reference of that global data, one function have some check routine and set that global data.
```c
void **sub_7FF6BBA420D0()
{
  ... // removing variable define
  if ( !dword_7FF6BBA5EDE4 )
  {
    v1 = &dword_7FF6BBA4F050 - (_UNKNOWN *)dword_7FF6BBA4593C;
    v2 = 0;
    i = 0i64;
    for ( i = 0i64; i < 7875; i += 225i64 )
    {
      v4 = &dword_7FF6BBA4593C[i];
      v5 = v1;
      v21 = &dword_7FF6BBA4593C[i];
      v6 = &MEMORY[0x7FF6BBA57304][i];
      v7 = 15i64;
      do
      {
        v8 = v6[1];
        v9 = v4;
        v10 = *v6;
        v11 = 15i64;
        v12 = *(v6 - 1);
        v13 = *(v6 - 2);
        v14 = *(v6 - 3);
        v15 = *(v6 - 4);
        do
        {
          v16 = *(int *)((char *)v9 + v5)
              - (v10 * *v9
               + *(v6 - 8) * *(v9 - 120)
               + *(v6 - 9) * *(v9 - 135)
               + *(v6 - 10) * *(v9 - 150)
               + *(v6 - 11) * *(v9 - 165)
               + *(v6 - 12) * *(v9 - 180)
               + *(v6 - 13) * *(v9 - 195)
               + v8 * v9[15]
               + v12 * *(v9 - 15)
               + v13 * *(v9 - 30)
               + v14 * *(v9 - 45)
               + v15 * *(v9 - 60)
               + *(v6 - 5) * *(v9 - 75)
               + *(v6 - 6) * *(v9 - 90)
               + *(v6 - 7) * *(v9 - 105));
          *(int *)((char *)v9 + v5) = v16;
          if ( v2 || v16 )
            v2 = 1;
          ++v9;
          --v11;
        }
        while ( v11 );
        v4 = v21;
        v6 += 15;
        v5 += 60i64;
        --v7;
      }
      while ( v7 );
      v1 = &dword_7FF6BBA4F050 - (_UNKNOWN *)dword_7FF6BBA4593C;
    }
    v17 = (void **)qword_7FF6BBA5EDF0;
    byte_7FF6BBA5F4F8 = v2; // << that global data, v2 should be 0
    dword_7FF6BBA5EDE4 = 1;
    do
    {
      v18 = 15i64;
      do
      {
        j_j_free(*v17);
        *v17++ = 0i64;
        --v18;
      }
      while ( v18 );
    }
    while ( (__int64)v17 < (__int64)&byte_7FF6BBA5F4F8 );
    result = (void **)Src;
    *(_QWORD *)&xmmword_7FF6BBA5F550 = Src;
  }
  return result;
}
```

## Solution
Simple z3 problem. Find input 0, 1 or 2 make that v16 is 0.

See [solve.py](./solve.py)

Implementing OCR for output is too annoying. Using better OCR called eyes.

## Flag
`ACSC{WELCOM3_T0_TH3_ACSC_W3_N33D_U}`

