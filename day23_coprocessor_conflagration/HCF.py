'''
Halt and Catch Fire
'''

import re


class HaltException(Exception):
    pass

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

class TabletComputer:
    def __init__(self, mem, debug=False):
        #self.pid = 'M%d'%pid
        self.pid = 'TC#'
        self.regs = {}# {'p':pid}
        self.mem = mem or []
        self.PC = 0
        self.sndOut = None
        self.recovered = None
        self.sendq = None#sendq
        self.recvq = None#recvq
        self.sendcount = 0
        self.state = 'EXEC'
        self.debug = debug
        self.mulcount = 0

    def write(self, *args):
        if self.debug:
            print('[%s]:' % self.pid, *args)

    def decode_val(self, v):
        if isinstance(v, int):
            return v
        val = self.regs.get(v)
        if val is None:
            self.regs[v] = 0
            val = 0
        return val

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
            raise HaltException("HALT")

        inst = self.mem[self.PC]
        #self.write(self.PC, inst, self.regs, self.state)
        name = inst[0]
        if name == 'snd':
            self.sndOut = self.decode_val(inst[1])
            if self.sendq is not None:
                self.sendq.append(self.sndOut)
                self.write('OUT', self.sndOut)
                self.sendcount += 1
            self.PC += 1
        #elif name == 'set':
        #    self.set_to_reg(inst[1], inst[2])
        #    self.PC += 1
        elif name == 'add':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a+b)
            self.PC += 1
        #elif name == 'mul':
        #    a = self.decode_val(inst[1])
        #    b = self.decode_val(inst[2])
        #    self.set_to_reg(inst[1], a*b)
        #    self.PC += 1
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
        elif name == 'set':
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], b)
            self.PC += 1
        elif name == 'sub':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a-b)
            self.PC += 1
        elif name == 'mul':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            self.set_to_reg(inst[1], a*b)
            self.mulcount += 1
            self.PC += 1
        elif name == 'jnz':
            a = self.decode_val(inst[1])
            b = self.decode_val(inst[2])
            if a != 0:
                self.PC += b
                self.write(' >> JUMP to', self.PC, '(offset', b,')')
                return
            self.PC += 1
        else:
            raise Exception('Instr: ', inst)
        self.write(self.PC, inst, self.regs, self.state)


def part1(instructions):
    comp = TabletComputer(mem=instructions, debug=False)
    
    while True:
        try:
            #input()
            comp.next()
        except HaltException as e:
            #if e.message == 'HALT':
            return comp.mulcount


def part2(instructions):
    comp = TabletComputer(mem=instructions, debug=False)
    comp.regs['a'] = 1
    while True:
        try:
            comp.next()     
        except HaltException as e:
            return comp.mulcount
        
    return comp.regs


import sys

instructions = load_input('test_input' if 'test' in sys.argv else 'input')


print('Part 1:', part1(instructions))
if 'bruteforce' in sys.argv:
    print('About to catch fire')
    print('Part 2:', part2(instructions))





