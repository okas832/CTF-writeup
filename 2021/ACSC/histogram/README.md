# Histogram
Pwnable, 200 points

## Description

[Link](https://histogram.chal.acsc.asia)

[Download](./histogram.tar.gz)

## Vulnerability
We can write NaN as input, and `ceil(nan)` returns 0.  
With these, `i` in `read_data` can be -1 so we can add 1 to memory which is on outside of `map`.

## Exploit
We can add small number in map[-1][0~29]. Thankfully, we can add some value in GOT section.  
GOT will save function's PLT address if corresponding library function did not called once.  
By add offset from function's PLT to `win` function, we can get a flag.

See [solve.py](./solve.py)
