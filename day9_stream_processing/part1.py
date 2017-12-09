
def read_input(input_file):
    with open(input_file) as inpf:
        return inpf.read().strip()


def calc_score(stream):
    stack = 0
    score = 0
    garbage = 0
    in_garbage = False
    ignore = False
    for i in range(0, len(stream)):
        c = stream[i]
        if ignore:
            ignore = False
            continue
        if in_garbage:
            if c == '!':
                ignore = True
                continue
            if c == '>':
                in_garbage = False
                continue
            garbage += 1
            continue
        if c == '{':
            # group start
            stack += 1
        elif c == '}':
            # group end
            score += stack
            stack -= 1
        elif c == '<':
            # garbage start
            in_garbage = True
        
    return (score, garbage)


print('Part 1: Group score is %d. Part 2: Garbage total: %d'%calc_score(read_input('input')))
