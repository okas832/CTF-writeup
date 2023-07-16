# mimikyu

Deja vu in Windows

[mimikyu](./mimikyu)

64 Teams solved.

## Solution

Loading library function in runtime is well-knwon in windows malware. You can statically analysis the logic of loader or just simply get them by debugging.

Rather than calculating values from `random`, inspecting them with gdb was much faster to me.

By solving multiprime RSA, we can get 4 bytes of flag in each iteration. 

## Flag

`zer0pts{L00k_th3_1nt3rn4l_0f_l1br4r13s!}`