# Sugar
Reversing, 170 points

# Description
[Download](./sugar.tar.gz)

# Analysis
There is an OVMF firmware. It gets a input and checks it.
In `disk.img`, there is one binary named BOOTX64.ELF(extracted with 7zip). This binary has core logic to get a flag.

Thankfully, there are some hardcoded error message that helps to analyze the function.
```c
// just pseudo code
print("Input flag: ");
flag = input(255);
print("\n");
if(strlen(flag) != 38 || input[0:4] != "ACSC{" || input[37] != "}")
{
  print("Wrong");
}
else
{
  // Ignore error parts
  EFI_HANDLE Handle;
  gBS->LocateDevicePath(&gEfiBlockIoProtocolGuid, // maybe?
                        "PciRoot(0x0)/Pci(0x1,0x1)/Ata(0x0)",
                        &Handle);
  EFI_BLOCK_IO_PROTOCOL *BlockIo;
  gBS->HandleProtocol (Handle, &gEfiBlockIoProtocolGuid, (VOID **) &BlockIo);
  BYTE buf[0x200];
  BlockIo->ReadBlocks (BlockIo, BlockIo->Media->MediaId, 1, 512, buf);
  ASSERT(*(QWORD *)buf == "EFI PART")

  Aes_ctx ctx;
  BYTE iv[16] = "\x00" * 16;
  BYTE key[16] = "\xA1\x86\x28\x23\x14\xBB\x20\x35\x3F\xEA\x9F\xB3\xB0\x9E\xF6\xCD";
  BYTE res[16];
  char ans[32];
  AesInit(&ctx, key, 128); // AES128
  AesCbcEncrypt(&ctx, ((QWORD *)buf)[8], 16, iv, res);
  StrHexToBytes(res, 32, ans, 16);
  if(!strcmp(ans, flag))
  {
    print("Correct!")
  }
  else
  {
    print("Wrong")
  }
}
```

Can know iv and key from binary, but have to get encrypted data from somewhere else.
There is `EFI PART` in disk, so able to guess that encrypted date is in it.

```
disk.img
00000200: 4546 4920 5041 5254 0000 0100 5c00 0000  EFI PART....\...
00000210: 2503 6894 0000 0000 0100 0000 0000 0000  %.h.............
00000220: ffff 0100 0000 0000 2200 0000 0000 0000  ........".......
00000230: deff 0100 0000 0000 5a50 4b64 d72a 3d4b  ........ZPKd.*=K
00000240: a40a a0fa 8e32 d35d 0200 0000 0000 0000  .....2.]........
```

So, encrypted data(buf[8]) is
```
\x5A\x50\x4B\x64\xD7\x2A\x3D\x4B\xA4\x0A\xA0\xFA\x8E\x32\xD3\x5D
```

Decrypt it will give proper input.
```python
from Crypto.Cipher import AES
import binascii

key = b"\xA1\x86\x28\x23\x14\xBB\x20\x35\x3F\xEA\x9F\xB3\xB0\x9E\xF6\xCD"
c = b"\x5A\x50\x4B\x64\xD7\x2A\x3D\x4B\xA4\x0A\xA0\xFA\x8E\x32\xD3\x5D"
iv = b"\x00" * 16

cipher = AES.new(key, AES.MODE_CBC, iv)
print(b"ACSC{" + binascii.hexlify(cipher.encrypt(c)) + b"}")
```

## flag
`ACSC{91e3de705dee881dcba84e840feb0e24}`

