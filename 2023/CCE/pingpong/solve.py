def get_key(O0000O0OOOO0OO0OO, O0OOOOO0O000OO0O0):
    O0O0O0OOOO0OOO0OO = [67, 32, 81, 69, 29, 41, 187, 13, 81, 157, 96, 219, 193, 68, 98, 67, 77, 58, 68, 62, 99, 92, 216, 25, 119, 181, 74]
    O0000O00O00O000O0 = [156, 234, 211, 1, 54, 153, 23, 4, 15, 2, 34, 97, 85, 34, 15, 20]
    OOO00O000OO000000 = 0
    O0O0OO000OO0OOOO0 = 0
    OOOO00OO00OO0O000 = []
    for OO00000O0O00O0O00 in O0O0O0OOOO0OOO0OO:
        OOOOO0OO0000OOO0O = (O0000O0OOOO0OO0OO + OOO00O000OO000000) % 16
        O000O0O00O00O000O = (O0OOOOO0O000OO0O0 + O0O0OO000OO0OOOO0) % 16
        OOOO00OO00OO0O000.append(chr(OO00000O0O00O0O00 ^ O0000O00O00O000O0[OOOOO0OO0000OOO0O] ^ O0000O00O00O000O0[O000O0O00O00O000O]))
        OOO00O000OO000000 = OOO00O000OO000000 + 1
        O0O0OO000OO0OOOO0 = O0O0OO000OO0OOOO0 + 1

    return "".join(OOOO00OO00OO0O000)

for i in range(16):
    for j in range(16):
        res = get_key(i, j)
        if res.startswith("cce2023{"):
            print(res)
            exit()
