from pwn import *

f = open("./sop_bytecode", "rb").read()

d = {
    218 : "set_tid_address",
    157 : "prctl",
    9 : "mmap",
    0 : "read",
    13: "sigaction",
    39 : "getpid",
    102 : "getuid",
    104 : "getgid",
    107 : "geteuid",
    186 : "gettid",
    110 : "getppid",
    108 : "getegid",
    111 : "getpgrp",
    57 : "fork",
    1 : "write"
}

mem = [0 for i in range(0x10)]
v_s = []
sw = False
buf = b""
cnt = 0

op_s = []
proc_name = ""
tmp_txt = ""
addr = 0
while len(f) != 0:
    c = u64(f[:8])

    syscall_no = c & 0xFF
    if syscall_no in d.keys():
        syscall = d[syscall_no]
    else:
        print(syscall_no)
        break
        
    c >>= 8

    arg = []
    argd = []
    for i in range(6):
        t = c & 0x3
        c >>= 2

        if t == 0:
            t = c & 0xF
            c >>= 4
            arg.append("reg[%d]"%t)
            argd.append(mem[t])
        elif t == 1:
            t = c & 0xF
            c >>= 4
            arg.append("&reg[%d]"%t)
            argd.append(t)
        elif t == 2:
            t = c & 0x1F
            c >>= 5
            v = c & ((1 << (t + 1)) - 1)
            c >>= t + 1
            arg.append(hex(v))
            argd.append(v)
        else:
            break

    #print(syscall, arg)
    if syscall == "set_tid_address":
        v_s.append(arg[0])
    elif syscall == "prctl":
        if argd[0] == 40:
            if arg[1][0] == "&":
                v_l = v_s.pop()
                #print(arg[1][1:], "=", v_l)
                op_s.append((arg[1][1:], 0, v_l, addr))
            else:
                v_l = v_s.pop()
                #if arg[1] != "0x217022":
                #    print("*(" + arg[1] + ")", "=", v_l)
                op_s.append((arg[1], 1, v_l, addr))
        elif argd[0] == 15:
            v_s.append(argd[1])
        elif argd[0] == 16:
            v_l = v_s.pop()
            op_s.append((arg[1][1:], 0, "*(" + hex(v_l) + ")",addr))
        else:
            for op in op_s:
                if op[1] == 0:
                    print(op[0], "=", op[2])
                else:
                    print("*(" + op[0] + ")", "=", op[2])
            op_s = []
            print(syscall, arg)

    elif arg[2] == "0x10":
        addr += 8
        f = f[8:]
        continue
    else:
        sss = 0
        #print(op_s)
        if syscall == "write":
            tmp_txt = "write" + str(arg)
        elif syscall == "read":
            tmp_txt = "read" + str(arg)
        elif syscall == "mmap":
            tmp_txt = "mmap" + str(arg)
        elif syscall == "sigaction":
            tmp_txt = "sigaction" + str(arg)
        elif syscall == "getgid":
            if arg[0] == "0x0":
                f = f[8:]
                addr += 8
                continue
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " & " + op_s[-1][2]
        elif syscall == "getuid":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " >> " + op_s[-1][2]
        elif syscall == "gettid":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " | " + op_s[-1][2]
        elif syscall == "getpid":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " + " + op_s[-1][2]
        elif syscall == "getegid":
            if len(op_s) == 1:
                sss = 1
                tmp_txt = op_s[-1][2][1:] + " = " + arg[0] + " - " + arg[1]
            else:
                sss = 3
                tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " - " + op_s[-1][2]
        elif syscall == "getpgrp":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " * " + op_s[-1][2]
        elif syscall == "getppid":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " << " + op_s[-1][2]
        elif syscall == "geteuid":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " ^ " + op_s[-1][2]
        elif syscall == "fork":
            sss = 3
            tmp_txt = op_s[-3][2][1:] + " = " + op_s[-2][2] + " / " + op_s[-1][2]
        else:
            print("!")
            print(syscall)
            break
        if sss != 0:
            op_s = op_s[:-sss]
        for op in op_s:
            if op[1] == 0:
                print(op[0], "=", op[2])
            else:
                print("*(" + op[0] + ")", "=", op[2])
        op_s = []
        if tmp_txt != "":
            print(tmp_txt)
        tmp_txt = ""
    f = f[8:]
    addr += 8
    
