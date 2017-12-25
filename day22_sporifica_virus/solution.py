'''

rotations

right - R(-Pi/2) 
left - R(Pi/2)

but since the Y-axis is flipped:

Rotate_left <=> rotate Pi/2
Rotate_right <=> rotate -Pi/2

Pi/2 rotation:

[x cos(t) - y sin(t), x sin(t) + y cos(t)]

t=Pi/2
[-y, x]

t=-Pi/2
[y, -x]

'''
import math


def rotate(v, t):
    return [int(round(v[0]*math.cos(t) - v[1]*math.sin(t))), int(round(v[0]*math.sin(t) + v[1]*math.cos(t)))]

def left(v):
    return rotate(v, -math.pi/2)

def right(v):
    return rotate(v, math.pi/2)
    
    
def read_input(f):
    m = []
    with open(f) as inpf:
        for line in inpf:
            m.append([0 if c=='.' else 1 for c in line.strip()])
    return m


def init_grid(m):
    grid = {}
    for y in range(0, len(m)):
        for x in range(0, len(m[y])):
            if m[y][x]:
                grid[(x,y)] = True
    
    return grid, (len(m[0])//2, len(m)//2)



def walk(grid, ip, iv, iters):
    p = ip
    d = iv
    infect_actions = 0
    while iters:
        gv = grid.get(p)
        if gv:
            d = right(d)
            del grid[p]
            # turn right, desinfect
        else:
            d = left(d)
            grid[p] = 1
            # turn left, infect
            infect_actions += 1
        
        p = (p[0]+d[0], p[1]+d[1])
        iters-=1
    return infect_actions


def walk_supervrus(grid, ip, iv, iters):
    '''
    we get all 1
    clean -> weak
    weak -> inf
    inf -> flag
    flag -> clean
    
    clean = None/0
    weak = 3
    inf = 1
    flag = 2
    
    '''
    INF = 1
    WEAK = 3
    FLAG = 2
    CLEAN = 0
    
    SM = {CLEAN:WEAK, WEAK: INF, INF: FLAG, FLAG: CLEAN}
    TRNS = {CLEAN: lambda v: left(v), WEAK: lambda v: v, INF: lambda v: right(v), FLAG: lambda v: [-v[0],-v[1]]}
    
    
    p = ip
    d = iv
    infect_actions = 0
    while iters:
        gv = grid.get(p)
        
        if gv is None:
            gv = CLEAN
        
        next_state = SM[gv]
        d = TRNS[gv](d)
        
        if next_state == INF:
            infect_actions += 1
        
        grid[p] = next_state
        
        p = (p[0]+d[0], p[1]+d[1])
        iters-=1
        if iters%1000 == 0:
            print(iters,'remaining')
    return infect_actions



grid, p = init_grid(read_input('input'))
print('Part 1: %d bursts of infection'% walk(grid,p, (0,-1), 10000))

grid, p = init_grid(read_input('input'))
print('Part 2: %d bursts of infection'% walk_supervrus(grid, p, (0, -1), 10000000))
