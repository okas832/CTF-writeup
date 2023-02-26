# Paper House

## Files

[safe.uf2](./safe.uf2)
[schematics.png](./schematics.png)

## Solution

First, make a binary from uf2(USB Flashing) format. You can use some converter from online or implement your own. It's not hard.

From strings, we can see "pico-sdk". So, we need to find `setup and loop`. Setup IDA's CPU to armv6 and with some `clicking c`, we can find it at `0x6c0` with it's CFG.

In `0x5D4`, it handles button click from `PmodKYPD`. It reads the signal and subtitute the input according to the table.

When user push 16 times, it checks the input at `0x580`. It generates the value from `Collatz conjecture` with initial value of 777.

Solution is easy. Generate 16 values and subtitute with the table.

[solve.py](./solve.py)