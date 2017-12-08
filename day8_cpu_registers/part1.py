import re
from collections import namedtuple

Inst = namedtuple('Instruction', ['target','action', 'value', 'cond', 'creg', 'cval'])

CONDS = {
    '>': lambda x,y: x > y,
    '<': lambda x,y: x < y,
    '>=': lambda x,y: x >= y,
    '==': lambda x,y: x == y,
    '<=': lambda x,y: x <= y,
    '!=': lambda x,y: x != y
}


def load_input(inp):
    instructions = []
    with open(inp) as inpf:
        for line in inpf:
            m = re.match('(?P<target>\\w+) (?P<action>\\w+) (?P<value>-?\\d+) if (?P<creg>\\w+) (?P<cond>[^\\s]+) (?P<cval>-?\\d+).*',line.strip())
            if m:
                target = m.group('target')
                action = m.group('action')
                value = int(m.group('value'))
                cond = m.group('cond')
                creg = m.group('creg')
                cval = int(m.group('cval'))
                instructions.append(Inst(target, action, value, cond, creg, cval))
            else:
                raise Exception('No match:', line)
    return instructions
                
def execute(instructions):
    regs = {}
    tmax = None
    for instr in instructions:
        if regs.get(instr.target) is None:
            regs[instr.target] = 0
        if regs.get(instr.creg) is None:
            regs[instr.creg] = 0
        cond = CONDS.get(instr.cond)
        if cond is None:
            raise Exception('Unknown condition %s. %s' %(instr.cond, instr))
        if cond(regs[instr.creg], instr.cval):
            if instr.action == 'inc':
                regs[instr.target] += instr.value
            elif instr.action == 'dec':
                regs[instr.target] -= instr.value
            else:
                raise Exception('Invalid action: %s' % instr)
        
        maxv = max([v for _,v in regs.items()])
        if tmax is None or tmax < maxv:
           tmax = maxv
    return regs, tmax
        
regs, alltime_max = execute(load_input('input'))
print('Part 1: Max regsiter value is:', max([v for _,v in regs.items()]))
print('Part 2: Max value at any time:', alltime_max)


