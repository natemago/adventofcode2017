import re

def load_input(f):
    instructions = []
    with open(f) as inpf:
        for line in inpf:
            parts = line.strip().split(' ')
            v = None
            if re.match('-{0,1}\\d+', parts[1]):
                parts[1] = int(parts[1])
            if len(parts) == 3:
                v = parts[2]
                if re.match('-{0,1}\\d+', parts[2]):
                    v = int(parts[2])
            instructions.append([parts[0], parts[1], v])
    return instructions

class SndComputer:
    def __init__(self, mem, pid=0, sendq=None, recvq=None, debug=False):
        self.pid = 'M%d'%pid
        self.regs = {'p':pid}
        self.mem = mem or []
        self.PC = 0
        self.sndOut = None
        self.recovered = None
        self.sendq = sendq
        self.recvq = recvq
        self.sendcount = 0
        self.state = 'EXEC'
        self.debug = debug

    def write(self, *args):
        if self.debug:
            print('[%s]:' % self.pid, *args)

    def decode_val(self, v):
        if isinstance(v, int):
            return v
        v = self.regs.get(v)
        if v is None:
            self.regs[v] = 0
            v = 0
        return v

    def set_to_reg(self, a, b):
        if self.regs.get(a) is None:
            self.regs[a] = 0
        if isinstance(b, int):
            self.regs[a] = b
            return
        v = self.regs.get(b)
        if v is None:
            self.regs[b] = 0
        self.regs[a] = v

    def next(self):
        if self.PC < 0 or self.PC >= len(self.mem):
            raise Exception("Halted")

        inst = self.mem[self.PC]
        self.write(self.PC, inst, self.regs, self.state, 'inq:', self.recvq, 'outq:', self.sendq)
        name = inst[0]
        if name == 'snd':
            self.sndOut = self.decode_val(inst[1])
            if self.sendq is not None:
                self.sendq.append(self.sndOut)
                self.write('OUT', self.sndOut)
                self.sendcount += 1
            self.PC += 1
        elif name == 'set':
            self.set_to_reg(inst[1], inst[2])
            self.PC += 1
        elif name == 'add':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a+b)
            self.PC += 1
        elif name == 'mul':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a*b)
            self.PC += 1
        elif name == 'rcv':
            if self.regs.get(inst[1]) is None:
                self.regs[inst[1]] = 0
            if self.regs[inst[1]] != 0:
                self.recovered = self.sndOut
            if self.recvq is not None:
                if len(self.recvq):
                    self.state = 'EXEC'
                    self.set_to_reg(inst[1], self.recvq[0])
                    self.recvq.remove(self.recvq[0])
                else:
                    self.state = 'WAIT'
                    return

            self.PC += 1
        elif name == 'mod':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a%b)
            self.PC += 1
        elif name == 'jgz':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            if a > 0:
                self.PC += b
                return
            self.PC += 1
        else:
            raise Exception('Instr: ', inst)

def part1(instructions):
    com = SndComputer(mem=instructions)

    while True:
        com.next()
        if com.recovered is not None:
            return com.recovered
        #input()


def part2(instructions):
    q1 = []
    q2 = []

    m0 = SndComputer(pid=0, mem=instructions, sendq=q1, recvq=q2)
    m1 = SndComputer(pid=1, mem=instructions, sendq=q2, recvq=q1)

    while True:
        if m0.state == 'WAIT' and m1.state == 'WAIT':
            print('Deadlock reached')
            return m1.sendcount
        m0.next()
        m1.next()

instructions = load_input('input')

print('Part1: ', part1(instructions))
print('Part2: ', part2(instructions))
