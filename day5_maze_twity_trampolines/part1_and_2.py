def read_input(file_name):
    instr = []
    with open(file_name) as inpf:
        for line in inpf:
            instr.append(int(line.strip()))
    return instr

def count_step(instructions):
    pc = 0
    cycles = 0
    while True:
        if pc < 0 or pc >= len(instructions):
            return cycles
        instr = instructions[pc]
        instructions[pc] += 1
        pc += instr
        cycles += 1
    return None # but we won't get here ever

def count_step_p2(instructions):
    pc = 0
    cycles = 0
    while True:
        if pc < 0 or pc >= len(instructions):
            return cycles
        instr = instructions[pc]
        if instr >= 3:
            instructions[pc] -= 1
        else:
            instructions[pc] += 1
        pc += instr
        cycles += 1

print('Part 1: ', count_step(read_input('input')))
print('Part 2: ', count_step_p2(read_input('input')))
