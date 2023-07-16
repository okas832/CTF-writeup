bc = bytes.fromhex("23384124435424435473243838414327412443547324383823514343435473232441243843435473233838514343244354732338384343542241732162940162B20162840139053F11F4FF2957810E406503003253323A395E57F3B4A38C7FBA07406503003153313A62670162850162570139B77380E1B07287F203406503003253323A393F68A3E4049A3B8F07406503003153313A623A01625801622A01395427B5B695525DCD0B406503003253323A3928919A4AA271379107406503003153313A620D01622B0162FD0039A3861405418C74E50B406503003253323A39BC61EDF2E96EC1AB06406503003153313A62E00062FE0062D0003988923AE0693F549206406503003253323A390FD1BEE339A196C505406503003153313A62B30062D10062A3003983EA7B97E54CD3EA06406503003253323A3987EFB0D15CFE86AD04406503003153313A62860062A4006276003919426CD4CAF6F2D909406503003253323A39EFFFDA1513EAAEDB06406503003153313A62590062770062490039FE1397DFCD127EF00A406503003253323A391CAFCF1F964541A506406503003153313A72233843254124384343546405003A3A637D003A395A883414A0C305BDFE3F648E00636B00323832383243324132617262420072623E00222241234343243841542438434354244354443852424331617262210072621D002222412343432438415424384343542443544438532241315243433161312338432343542241670F002438432443254124435468020031612325432441233843435473232441243843435473222341243843435473632100232245412438384343435473243826234124414343547323384324435473630000233843547371")

idx = 0
while idx < 635:
    op = bc[idx]

    if 0x62 <= op and op <= 0x6f:
        imm = bc[idx + 2] * 0x100 + bc[idx + 1]

    if op == 0x21:
        print("%03d : PUSH 0"%(idx))
        idx += 1
    elif op == 0x22:
        print("%03d : PUSH 1"%(idx))
        idx += 1
    elif op == 0x23:
        print("%03d : PUSH pi"%(idx))
        idx += 1
    elif op == 0x24:
        print("%03d : PUSH log_2 10"%(idx))
        idx += 1
    elif op == 0x25:
        print("%03d : PUSH log_2 e"%(idx))
        idx += 1
    elif op == 0x26:
        print("%03d : PUSH log_10 2"%(idx))
        idx += 1
    elif op == 0x27:
        print("%03d : PUSH log_e 2"%(idx))
        idx += 1
    elif op == 0x31:
        print("%03d : fxch  st(1)"%(idx))
        idx += 1
    elif op == 0x32:
        print("%03d : fxch  st(2)"%(idx))
        idx += 1
    elif op == 0x33:
        print("%03d : fxch  st(3)"%(idx))
        idx += 1
    elif op == 0x34:
        print("%03d : fxch  st(4)"%(idx))
        idx += 1
    elif op == 0x35:
        print("%03d : fxch  st(5)"%(idx))
        idx += 1
    elif op == 0x36:
        print("%03d : fxch  st(6)"%(idx))
        idx += 1
    elif op == 0x37:
        print("%03d : fxch  st(7)"%(idx))
        idx += 1
    elif op == 0x38:
        print("%03d : dup"%(idx))
        idx += 1
    elif op == 0x39:
        dat = bc[idx + 1: idx + 11]
        print("%03d : push %s "%(idx, str(list(dat))))
        idx += 11
    elif op == 0x3A:
        print("%03d : pop"%(idx))
        idx += 1
    elif op == 0x41:
        print("%03d : faddp   st(1), st"%(idx))
        idx += 1
    elif op == 0x42:
        print("%03d : fsubp   st(1), st"%(idx))
        idx += 1
    elif op == 0x43:
        print("%03d : fmulp   st(1), st"%(idx))
        idx += 1
    elif op == 0x44:
        print("%03d : fdivp   st(1), st"%(idx))
        idx += 1
    elif op == 0x45:
        print("%03d : fchs   st(1), st"%(idx))
        idx += 1
    elif op == 0x51:
        print("%03d : fsqrt   st(1), st"%(idx))
        idx += 1
    elif op == 0x52:
        print("%03d : fsin   st(1), st"%(idx))
        idx += 1
    elif op == 0x53:
        print("%03d : fcos  st(1), st"%(idx))
        idx += 1
    elif op == 0x54:
        print("%03d : frndint   st(1), st"%(idx))
        idx += 1
    elif op == 0x61:
        print("%03d : ret"%(idx))
        idx += 1
    elif op == 0x62:
        print("%03d : call %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x63:
        print("%03d : jump %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x64:
        print("%03d : je %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x65:
        print("%03d : jne %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x66:
        print("%03d : jae %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x67:
        print("%03d : ja %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x68:
        print("%03d : jbe %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x69:
        print("%03d : jb %03d"%(idx, idx + imm + 3))
        idx += 3
    elif op == 0x71:
        print("%03d : hlt"%(idx))
        idx += 1
    elif op == 0x72:
        print("%03d : ipt"%(idx))
        idx += 1
    elif op == 0x73:
        print("%03d : opt"%(idx))
        idx += 1
    
