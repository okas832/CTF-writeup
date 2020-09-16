# harmagedon

### Binary

By removing the code of printing, choosing the characters, we can simplify this problem to math problem.

```python
v0 = 0
for _ in range(11):
    if v0 == 0xB77C7C:
        # need to reach here
        break
    ipt = select_0_to_3()
    v0 = 4 * (v0 + ipt + 1)
```

### Solution

We can easily know that we have to select number 11 times by bit length of `0xB77C7C`.

There is a recurrence relation of v0 and we know the depth. So, we can derive the formula of v0's value,

![formula](https://render.githubusercontent.com/render/math?math=v0=\sum_{n=1}^{11}4^{n}\times%20ipt_{12-n}%2b4^{n})

where ![formula](https://render.githubusercontent.com/render/math?math=ipt_{i}) means i th input.

Whatever the ![formula](https://render.githubusercontent.com/render/math?math=ipt_{i}) values are, there is ![fomular](https://render.githubusercontent.com/render/math?math=\sum_{n=1}^{11}4^{n}=0\textrm{x}555554) that always adds to v0.

```
0xB77C7C - 0x555554 = 0x622728
```

![formula](https://render.githubusercontent.com/render/math?math=ipt_{i}) are two bits value and ![formula](https://render.githubusercontent.com/render/math?math=4^n) shifts left twice.

```
     ipt       1  2  3  4  5  6  7  8  9 10 11         
0x622728 = 0b 01 10 00 10 00 10 01 11 00 10 10 00
  choose       1  2  0  2  0  2  1  3  0  2  2
```

![ans.img](./img/ans.png)

 