# Check in Abyss

## Files

[bios.bin](./bios.bin)
[bzImage](./bzImage)
[rootfs.cpio](./rootfs.cpio)
[run.sh](./run.sh)

## Solution

`delver` binary raises System Management Interrupt (SMI) by send output to 0xB2 I/O port. Which means we should find the SMM code in the bios.

In `0xFFFEFF4E` in bios, there is a handler. And we can check there is a specific handler for `al == 0x77` at `0xFFFF01B1` and `al == 0xFF` at `0xFFFF0210`.

When `al == 0x77`, it schedules the table at `0xA1000` like stream cipher.
When `a1 == 0xFF`, it encrypts the input and compare with the constant array.

See `src/fw/smm.c` from `seabios`([link](https://github.com/coreboot/seabios/blob/e4f02c12518c0fe8154950b2e34c56a92721626e/src/fw/smm.c)) for how they control the registers.

[solve.py](./solve.py)