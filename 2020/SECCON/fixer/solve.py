b = 13611142019359843741091679554812914051545792465993098606064046040462991
def a(x):
    if x == 0:
            return 1
    return ((x + 1) * a(x-1) + 7) & 0xFF

lst = []
for i in range(26):
    lst.append(a(i))

ans = ""
while b:
    ans += chr(lst.index(b % 257) + 65)
    b //= 257

print("SECCON{" + ans + "}")
