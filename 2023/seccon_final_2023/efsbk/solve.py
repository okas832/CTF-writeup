f = open("flag.bin", "rb").read()

e = 0x10001
p = 0xf4745279de19f82d3d37a68c0e9371cd22e700686ff51687d5838ec88661b0523692fdeb49a9becb33ed0ecabdf0ab9b854542ce64e09e3153f8d19056ab1437e069722177b7b0f078cb93a1f108d588bda873c298815d9382f02b87412f9e00d1cc88276091230e22fdddcc071b0c8ad1048e404bb3185a1d92d21eda2e8017
q = 0xf8ea198e5cbad66b2dfc5b3ec0475285e67beb3ea1dc227078fb452cd0e7d240f14610ebedd98f5130c1f94e6a311019d7242e19ea3b723e3d44ff8b0684bc6edac0ba3999e4f7998e26dfb7e24a28f598bdd610d2d5bd2a2a1744a6aca7a9a5b3ea5c50b41a0639bd5dbea97e35e2e536fe30ea6d3c1e4c293db861fa53b667

n = p * q
d = pow(e, -1, (p - 1) * (q - 1))

c = f[0x1E8:0x2E8]
c = int.from_bytes(c, byteorder = "little")

m = pow(c, d, n)
m = m.to_bytes(256, "little")
k = m[:32][::-1]

cc = f[0x514:0x914]

from Crypto.Cipher import AES

# https://diyinfosec.medium.com/symmetric-key-usage-in-efs-81924bee27ab
cipher = AES.new(k, AES.MODE_CBC, iv = bytes.fromhex("121316e97b65165861899144bead8919"))
print(cipher.decrypt(cc[:512]).decode("utf-8"))
cipher = AES.new(k, AES.MODE_CBC, iv = bytes.fromhex("121516e97b651658618b9144bead8919"))
print(cipher.decrypt(cc[512:]).decode("utf-8"))
