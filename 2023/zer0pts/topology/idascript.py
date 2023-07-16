import ida_search
import idautils
import struct
def ROL(data, shift, size=64):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size )
    return (body + remains)
    

def ROR(data, shift, size=64):
    shift %= size
    body = data >> shift
    remains = (data << (size - shift)) - (body << size)
    return (body + remains)

addr = 0x1000

f_lst = list(idautils.Functions())

dic = {}

while True:
    cmp_addr = ida_search.find_text(addr, 0, 0, "cmp     rax, rdx", SEARCH_DOWN)
    now_addr = cmp_addr
    
    insn = DecodePreviousInstruction(now_addr)
    if not insn:
        break
    now_addr = insn.ea
    
    res = int(GetDisasm(now_addr).split(", ")[1][:-1], 16)
    stop = False
    while True:
        insn = DecodePreviousInstruction(now_addr)
        now_addr = insn.ea
        op = GetDisasm(now_addr).split(" ")[0]
        
        if GetDisasm(now_addr).find("[rdi]") != -1:
            stop = True
        if op == "ror":
            sft = GetDisasm(now_addr).split(";")[0].split(", ")[-1]
            if sft == "cl":
                sft = "ecx"
            tmp_addr = now_addr
            while True:
                insn = DecodePreviousInstruction(tmp_addr)
                tmp_addr = insn.ea
                tmp_op = GetDisasm(tmp_addr).split(" ")[0]
                if tmp_op == "mov":
                    reg = GetDisasm(tmp_addr).split(";")[0].split(", ")[0].split(" ")[-1]
                    if reg == sft:
                        sft = GetDisasm(tmp_addr).split(";")[0].split(", ")[-1]
                        try:
                            if sft.find("h") == -1:
                                sft = int(sft.strip())
                            else:
                                sft = int(sft.strip()[:-1], 16)
                            break
                        except:
                            continue
            res = ROL(res, sft)
        elif op == "rol":
            sft = GetDisasm(now_addr).split(";")[0].split(", ")[-1]
            if sft == "cl":
                sft = "ecx"
            tmp_addr = now_addr
            while True:
                insn = DecodePreviousInstruction(tmp_addr)
                tmp_addr = insn.ea
                tmp_op = GetDisasm(tmp_addr).split(" ")[0]
                if tmp_op == "mov":
                    reg = GetDisasm(tmp_addr).split(";")[0].split(", ")[0].split(" ")[-1]
                    if reg == sft:
                        sft = GetDisasm(tmp_addr).split(";")[0].split(", ")[-1]
                        try:
                            if sft.find("h") == -1:
                                sft = int(sft.strip())
                            else:
                                sft = int(sft.strip()[:-1], 16)
                            break
                        except:
                            continue
            res = ROR(res, sft)
        elif op == "bswap":
            res = struct.unpack("<Q", struct.pack(">Q", res))[0]
        elif op == "xor":
            insn = DecodePreviousInstruction(now_addr)
            now_addr = insn.ea
            imm = GetDisasm(now_addr).split("; ")[0].split(", ")[-1]
            if imm.find("h") == -1:
                imm = int(imm)
            else:
                imm = int(imm.strip()[:-1], 16)
            res = res ^ imm
        elif op == "add":
            insn = DecodePreviousInstruction(now_addr)
            now_addr = insn.ea
            imm = GetDisasm(now_addr).split("; ")[0].split(", ")[-1]
            if imm.find("h") == -1:
                imm = int(imm)
            else:
                imm = int(imm.strip()[:-1], 16)
            res = res - imm
            if res < 0:
                res += 1 << 64
        if stop:
            break
    
    for i in range(len(f_lst) - 1):
        if f_lst[i] <= cmp_addr and cmp_addr <= f_lst[i + 1]:
            f_name = ida_funcs.get_func_name(f_lst[i])
    
    dic[f_name] = dic.get(f_name, []) + [res]
    
    addr = cmp_addr + 3
        
flag = b""
for i in range(10):
    dic2 = {}
    for k, v in dic.items():
        if i >= len(v):
            continue
        dic2[v[i]] = dic2.get(v[i], 0) + 1
    s = sorted(list(dic2.items()), key=lambda x: x[1])
    print(s)
    flag += s[-1][0].to_bytes(8, 'little')
 
print(flag)