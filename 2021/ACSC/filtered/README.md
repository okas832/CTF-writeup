# Filtered
Pwnable, 100points

## Description
```
Filter invalid sizes to make it secure!
nc filtered.chal.acsc.asia 9001
```

[Download](./filtered.tar.gz)

## Vulnerability
Variable `length` in `main` is signed int, but argument `length` in `readline` is unsigned int.  
So when we give negative value to length, the check will pass and readline can write more than 0x100 bytes on `buf` in main.

## Exploit
We can simply overwrite return address of `main` to `win` function.

See [solve.py](./solve.py)
