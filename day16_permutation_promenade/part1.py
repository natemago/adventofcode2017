import re

NAMES = lambda: [chr(ord('a') + i) for i in range(0,16)]

def read_input(inf):
    moves = []
    with open(inf) as inpf:
        for move in inpf.read().strip().split(','):
            move = move.strip().lower()
            if move[0] == 's':
                moves.append( ('s', int(move[1:]), 0) )
            else:
                values = move[1:].split('/')
                if move[0] == 'x':
                    moves.append( ('x', int(values[0]), int(values[1])) )
                else:
                    moves.append( ('p', values[0],values[1]))
    return moves

def dance(programs, moves):
    for move, value1, value2 in moves:
        #print(move, value1, value2)
        if move == 's':
            #print('S:', programs)
            lastN = programs[-value1:]
            programs = lastN + programs[:-value1]
            #print('  ->', programs)
        elif move == 'x':
            #print('X:', programs)
            programs[value1], programs[value2] = programs[value2], programs[value1]
            #print('  ->', programs)
        else:
            #print('P:', programs)
            i1 = programs.index(value1)
            i2 = programs.index(value2)
            programs[i1] = value2
            programs[i2] = value1
            #print('  ->', programs)
    return programs
    

def detect_cycle(programs, moves):
    i = 1
    orig_seq = NAMES()
    while True:
        programs = dance(programs, moves)
        print(''.join(programs), '==', ''.join(orig_seq))
        if programs == orig_seq:
            return i
        i += 1
        if i % 1000 == 0:
            print('At',i,'but no cycle yet.')
    return None

def dance_for(programs, moves, dances):
    for i in range(0, dances):
        programs = dance(programs, moves)
        print(i, ''.join(programs))
    return ''.join(programs)

def part2(cycle_length, programs, moves):
    return dance_for(programs, moves, (10**12)%cycle_length)

print('Test: ', dance(['a','b','c','d','e'],[('s', 1, 0),('x',3, 4),('p','e', 'b')]))
print('Part 1: Programs after dance: ', ''.join(dance(NAMES(), read_input('input'))))

cl = detect_cycle(NAMES(), read_input('input') )
print('Detected cycle at:', cl)
print('Part 2:', part2(cl, NAMES(), read_input('input') ))
            