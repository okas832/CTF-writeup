enc = list(map(int, "27777890035288 498454011879264 190392490709135 16641027750620563662096 83621143489848422977 1500520536206896083277 1779979416004714189 22698374052006863956975682 573147844013817084101 5358359254990966640871840 218922995834555169026 1264937032042997393488322 483162952612010163284885 573147844013817084101 31940434634990099905 26925748508234281076009 8670007398507948658051921 31940434634990099905 26925748508234281076009 573147844013817084101 483162952612010163284885 483162952612010163284885 8670007398507948658051921 31940434634990099905 927372692193078999176 16641027750620563662096 32951280099 1500520536206896083277 31940434634990099905 7778742049 781774079430987230203437 31940434634990099905 3311648143516982017180081 32951280099 483162952612010163284885 31940434634990099905 43566776258854844738105 4807526976 781774079430987230203437 31940434634990099905 26925748508234281076009 8670007398507948658051921 31940434634990099905 927372692193078999176 32951280099 1264937032042997393488322 16641027750620563662096 781774079430987230203437 59425114757512643212875125".split(" ")))

lst = [0, 1]
for i in range(2, 0x100):
    lst.append(lst[-1] + lst[-2])

flag = []
for i in enc:
    flag.append(lst.index(i))

print(bytes(flag))



