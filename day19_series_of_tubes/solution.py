def read_input(f):
    grid = []
    with open(f) as inpf:
        for line in inpf:
            grid.append([c for c in line])
    return grid
    

MN = {(-1,0):'up', (0,1):'right', (1,0):'down', (0,-1):'left'}

def follow_diagram(diagram):
    moves = [[-1,0], [0,1], [1,0], [0,-1]] # up, right, down, left
    
    y = 0
    x = diagram[0].index('|')
    #print(diagram)
    #print(y, x)
    
    d = [1,0] # initial direction, down
    
    code = ''
    total_steps = 1
    while True:
        #print(x,y,diagram[y][x])
        steps = 0
        while True:
            dx, dy = x+d[1], y+d[0]
            
            if dy >= 0 and dy < len(diagram) and dx >= 0 and dx < len(diagram[dy]):
                #print(dy, dx, ' ',diagram[dy][dx])
                if not diagram[dy][dx] in ['+', ' ']:
                    x,y = dx, dy
                    steps += 1
                    if diagram[y][x].isalpha():
                        code += diagram[y][x]
                
                else:
                    if diagram[dy][dx] == '+':
                        steps += 1
                        x,y = dx,dy
                    break
            else:
                break
        
        #print('at ', diagram[y][x])
        print(MN[(d[0],d[1])], steps)
        total_steps += steps
        dir_found = False
        
        for move in moves:
            #print(move, '==', [-d[0], -d[1]])
            if move == [-d[0], -d[1]]:
                #print('  yep')
                continue
            dx, dy = x+move[1], y+move[0]
            
            if dy >= 0 and dy < len(diagram) and dx >= 0 and dx < len(diagram[dy]):
                #print(diagram[dy][dx], "diagram[dy][dx] in ['|', '-']=", diagram[dy][dx] in ['|', '-'], "diagram[dy][dx].isalpha()=",diagram[dy][dx].isalpha())
                if diagram[dy][dx] in ['|', '-'] or diagram[dy][dx].isalpha():
                    d = move
                    dir_found = True
                    break
        
        if not dir_found:
            break
    return code, total_steps


test_diag= '     |          ,     |  +--+    ,     A  |  C    , F---|----E|--+ ,     |  |  |  D ,     +B-+  +--+ '


print('Test:', follow_diagram([[c for c in s] for s in test_diag.split(',')]))
code, steps = follow_diagram(read_input('input'))
print('Part1: ', code)
print('Part2: ', steps)
