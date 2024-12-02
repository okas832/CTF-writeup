import pickle, sys

class VM:
    def __init__(self):
        self.program = []   
        self.running = True
        self.call_stack = []   
        self.labels = {}     

    def load_program(self, bytecode):
        self.program = bytecode[:-1]
        real_program = []

        # optimize +1 thing
        for i in self.program:
            real_program.append(i)
            if len(real_program) >= 3 and  real_program[-3][0] == 102 and real_program[-2][0] == 102 and real_program[-1][0] == 2:
                sm = real_program[-3][1] + real_program[-2][1]
                real_program.pop()
                real_program.pop()
                real_program.pop()
                real_program.append([102, sm])

        self.program = real_program
        for instruction in self.program:
            opcode, *operands = instruction
            if opcode == 0x66:
                print("push %d"%operands[0])
            elif opcode == 0x44:
                print("pop")
            elif opcode == 0x02:
                print("add")
            elif opcode == 0x99:
                print("jz %d"%(operands[0] + 1))
            elif opcode == 0x9:
                print("cmple")
            elif opcode == 0x63:
                print("sub")
            elif opcode == 0x32:
                print("xor")
            elif opcode == 0x79:
                print("mul")
            elif opcode == 0x54:
                print("push_var %s"%operands[0])
            elif opcode == 0x77:
                print("pop_var %s"%operands[0])
            elif opcode == 0x17:
                print("jz %d"%(operands[0] - 1))
            elif opcode == 0x1:
                print("call %s"%operands[0])
            elif opcode == 0x3:
                print("ret")
            elif opcode == 0x8:
                print("hlt")


vm = VM()
vm.load_program(pickle.loads(open('code.bin', 'rb').read()))