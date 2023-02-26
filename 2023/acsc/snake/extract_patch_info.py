change_signal = "_BYTE *__fastcall sub_42EC6F(_QWORD *a1)"
d = {}

f = open("snake.c", "r").readlines()

state = 0  # 0 : many xor format, 1 : last function of 0's format, 2 : ptrace peek poke
k = None
info = []
bidx = -1

for i in f:
    i = i.strip()
    if i == change_signal:
        state = 1

    if state == 0:
        if k == None and i.startswith("if ( a1[10] != "):
            k = i.split(" ")[4].replace("L", "")
            if k.startswith("0x"):
                k = int(k, 16)
            else:
                k = int(k)
        elif k != None:
            if i.startswith("v2 = (_BYTE *)(a1[5] ^ "):
                v = i.split(" ")[5].split(")")[0].replace("L", "")
                if v.startswith("0x"):
                    v = int(v, 16)
                else:
                    v = int(v)
                info.append(v)
                info.append(0)
            if i.startswith("*v2 ") or i.startswith("v2["):
                idx, op, v = i.split(" ")

                if idx[0] == "*":
                    idx = 0
                else:
                    idx = int(idx[3:-1])
                while bidx + 1 != idx:
                    info.append(("+", 0))
                    bidx += 1
                bidx = idx

                v = v.replace("u", "").replace(";", "")
                if v.startswith("~"):
                    op = "~"
                    v = 0
                elif v.startswith("0x"):
                    v = int(v, 16)
                else:
                    v = int(v)
                info.append((op[0], v))
            if i.startswith("++") or i.startswith("--"):
                idx = int(i[5:-2])
                while bidx + 1 != idx:
                    info.append(("+", 0))
                    bidx += 1
                bidx = idx
                if i[0] == "+":
                    info.append(("+", 1))
                if i[0] == "-":
                    info.append(("-", 1))
                    
            if i.startswith("return result"):
                d[k] = info
                info = []
                k = None
                bidx = -1
                
    if state == 1:
        if k == None and i.startswith("if ( result == (_BYTE *)"):
            k = 8392
        elif k != None:
            if i.startswith("v2 = (_BYTE *)(a1[5] ^ "):
                v = i.split(" ")[5].split(")")[0].replace("L", "")
                if v.startswith("0x"):
                    v = int(v, 16)
                else:
                    v = int(v)
                info.append(v)
                info.append(0)
            if i.startswith("*v2 ") or i.startswith("v2["):
                _, op, v = i.split(" ")

                v = v.replace("u", "").replace(";", "")
                if v.startswith("~"):
                    op = "~"
                    v = 0
                elif v.startswith("0x"):
                    v = int(v, 16)
                else:
                    v = int(v)
                info.append((op[0], v))
            if i.startswith("return result"):
                d[k] = info
                info = []
                k = None
                state = 2
    if state == 2:
        if k == None and (i.startswith("if ( *(_QWORD *)(a1 + 80) != ") or i.startswith("if ( a1->rax !=")):
            k = i.split(" ")[-2].replace("L", "")
            if k.startswith("0x"):
                k = int(k, 16)
            else:
                k = int(k)
            info.append(0)
            info.append(1)
        elif k != None:
            c = i.split(" ")
            if len(c) >= 2 and (c[-2] == "^" or c[-2] == "-" or c[-2] == "+"):
                v = c[-1].replace("L","").replace(";","").replace(")","")
                if v.startswith("0x"):
                    v = int(v, 16)
                else:
                    v = int(v)
                info.append((c[-2], v))
            if i == "}":
                d[k] = info
                info = []
                k = None

with open("a.py", "wt") as f:
    f.write(str(d))
    
