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
    def __init__(self, mem, pid=0, on_send=None, on_recv=None):
        self.pid = pid
        self.regs = {'p':pid}
        self.mem = mem or []
        self.PC = 0
        self.sndOut = None
        self.recovered = None
        self.on_send = on_send
        self.on_recv = on_recv

    def decode_val(self, v):
        if isinstance(v, int):
            return v
        v = self.regs.get(v)
        if v is None:
            self.regs[v] = 0
            v = 0
        return v

    def set_to_reg(self, a, b):
        #print(a, '<-', b)
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

        for k,v in self.regs.items():
            if k is None:
                print(self.pid, inst, self.regs)
                raise Exception('None reg name. Bug.')

        print('[M%d]:'%self.pid,self.PC, inst, self.regs)

        name = inst[0]
        if name == 'snd':
            self.sndOut = self.decode_val(inst[1])
            if self.on_send:
                self.on_send(self, self.sndOut)
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
                #print('Recovered: ', self.recovered)
            if self.on_recv:
                self.on_recv(self, inst[1])
            self.PC += 1
        elif name == 'mod':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a%b)
            self.PC += 1
        elif name == 'jgz':
            print(self.pid,'->', self.regs)
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            print(self.pid,'-->', self.regs)
            if a > 0:
                #print('jump: ', b, '; PC=', self.PC)
                self.PC += b
                return
            self.PC += 1
        else:
            raise Exception('Instr: ', inst)

def part1(instructions):
    com = SndComputer(mem=instructions)

    while True:
        com.next()
        print(com.regs)
        if com.recovered is not None:
            return com.recovered
        #input()


def part2(instructions):
    M = {'m0': {'snd': [], 'rcv': [], 'state': 'ok', 'count': 0}, 'm1': {'snd': [], 'rcv': [], 'state': 'ok', 'count': 0}}

    def on_send(m, val):
        #print(m.pid, 'sends', val)
        opid = 'm0' if m.pid == 1 else 'm1'
        pid = 'm%d'%m.pid
        M[pid]['snd'].append(val)
        if M[opid]['state'] == 'wait_rcv' and M[opid]['wait_rcv']:
            on_recv(M[opid]['machine'], M[opid]['wait_rcv'])
        M[pid]['count'] += 1

    def on_recv(m, reg):
        #print(m.pid, 'waits val in', reg)
        opid = 'm0' if m.pid == 1 else 'm1'
        pid = 'm%d'%m.pid
        if len(M[opid]['snd']):
            val = M[opid]['snd'][0]
            M[opid]['snd'] = M[opid]['snd'][1:]
            m.set_to_reg(reg, val)
            M[pid]['state'] = 'ok'
            return

        M[pid]['state'] = 'wait_rcv'
        M[pid]['wait_rcv'] = reg

    m0 = SndComputer(pid=0, mem=instructions, on_send=on_send, on_recv=on_recv)
    m1 = SndComputer(pid=1, mem=instructions, on_send=on_send, on_recv=on_recv)

    M['m0']['machine'] = m0
    M['m1']['machine'] = m1

    while True:
        #print(M['m0'])
        #print(M['m1'])
        if M['m0']['state'] == 'wait_rcv' and M['m1']['state'] == 'wait_rcv':
            print('Deadlock')
            print(M)
            break
        if M['m0']['state'] == 'ok':
            m0.next()
        else:
            print('M0 waits')
        if M['m1']['state'] == 'ok':
            m1.next()
        else:
            print('M1 waits')
        #input()


instructions = load_input('test_input_p2')
instructions = load_input('input')

#print('Part1: ', part1(instructions))
print('Part2: ', part2(instructions))
