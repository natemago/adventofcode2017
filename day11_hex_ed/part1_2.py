
def move_odd_even(v, odd, even):
    return even if abs(v) % 2 == 0 else odd

MOVES = {
    'n':  lambda x,y: [0, -1],
    'nw': lambda x,y: move_odd_even(x, [-1, -1],[-1, 0]),
    'ne': lambda x,y: move_odd_even(x, [1,-1],[1, 0]),
    'sw': lambda x,y: move_odd_even(x, [-1,0],[-1,1]),
    's':  lambda x,y: [0, 1],
    'se': lambda x,y: move_odd_even(x, [1,0],[1,1])
}


def read_input(fn):
    with open(fn) as inpf:
        return [m.strip().lower() for m in inpf.read().strip().split(',')]

def walk(moves):
    memz = {}
    x = 0
    y = 0
    max_steps = 0
    last_steps = 0
    for move in moves:
        if not move:
            raise Exception('Woops, dirty input - empty move')
        movefn = MOVES.get(move)
        if not movefn:
            raise Exception('Unknown move: %s'%move)
        dv = movefn(x,y)
        x += dv[0]
        y += dv[1]

        steps = memz.get((x,y))
        if steps is None:
            steps = dist( (0,0), (x,y))
            memz[(x,y)] = steps
        if steps >= max_steps:
            max_steps = steps
        last_steps = steps
    return last_steps, max_steps, (x,y)


def dist(p1, p2):
    ms = [(p2,m) for _,m in MOVES.items()]
    steps = 0
    while True:
        nms = []
        #print([m[0] for m in ms])
        sol = []
        for pm in ms:
            p = pm[0]
            if p[0] == p1[0]:
                sol.append(steps + abs(p[1] - p1[1]))
            if p[1] == p1[1]:
                sol.append(steps + abs(p[0] - p1[0]))
            dv = pm[1](p[0],p[1])
            nms.append( ( (p[0] + dv[0], p[1] + dv[1]), pm[1]) )
        if len(sol) > 0:
            return min(sol)
        steps += 1
        ms = nms

    return None


print('Part1, minimal steps: %d. Part 2, max steps: %d. Last position on grid: %s' % walk(read_input('input')))
