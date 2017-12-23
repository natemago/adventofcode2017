import math


class Rule:
    def __init__(self, n, inp, out):
        self.inp = inp
        self.out = out
        self.n = n
        self.size = len(inp)
    
    def keys(self):
        rotations= [lambda m: m, lambda m: rotate_mx(m, math.pi/2), lambda m: rotate_mx(m, math.pi), lambda m: rotate_mx(m, -math.pi/2)]
        flips = [lambda m: m, lambda m: fliph(m), lambda m: flipv(m)]
        keys = set()
        for flip in flips:
            m = flip(self.inp)
            for rot in rotations:
                keys.add(mstr(rot(m),'|'))
        return keys
   
    def __repr__(self):
        return 'R(%d, %d)'%(self.n,self.size)
    def __str__(self):
        return self.__repr__()


def vadd(v, dv):
    rv = []
    for i in range(0, len(v)):
        rv.append(v[i]+dv[i])
    return rv

def rotate(v, ang):
    return [v[0]*math.cos(ang) - v[1]*math.sin(ang), v[0]*math.sin(ang) + v[1]*math.cos(ang)]

def rotate_mx(mx, ang):
    rm = []
    tr = (len(mx)-1)/2
    for y in range(0, len(mx)):
        row = []
        rm.append(row)
        for x in range(0, len(mx[y])):
            p = [x,y]
            #print(p, vadd(p, [-tr, -tr]), rotate(vadd(p, [-tr, -tr]), ang))
            p = vadd(rotate(vadd(p, [-tr, -tr]), ang), [tr, tr])
            row.append(mx[round(p[1])][round(p[0])])
    
    return rm

def fliph(m):
    rm = [r for r in m]
    for i in range(0, len(m)//2):
        rm[i],rm[len(m)-1-i] = rm[len(m)-1-i],rm[i]
    return rm

def flipv(m):
    m = rotate_mx(m, math.pi/2)
    m = fliph(m)
    return rotate_mx(m, -math.pi/2)
            
def mstr(m,rowend='\n'):
    s = []
    for r in m:
        s.append(''.join(r))
    return rowend.join(s)

def read_input(f):
    rules = []
    i= 0
    with open(f) as inpf:
        for line in inpf:
            rps = line.strip().split(' => ')
            inp = rps[0].strip()
            out = rps[1].strip()
            
            ins = inp.split('/')
            outs = out.split('/')
            
            r = Rule(n=i, inp=[[c for c in r] for r in ins], out=[[c for c in r] for r in outs])
            rules.append(r)
            i += 1
    return rules



def get_rulebook(rules):
    rulebook = {}
    
    for r in rules:
        rbook = {}
        for key in r.keys():
            rbook[key] = r
            if rulebook.get(key):
                raise Exception('Key [%s] already defined for rule %s'%(key, rulebook.get(key)))
        rulebook.update(rbook)
    
    return rulebook


def split(m, s):
    n = len(m)//s
    gg = []
    
    for i in range(0, n):
        gr = []
        gg.append(gr)
        for j in range(0, n):
            mm = []
            gr.append(mm)
            for ii in range(0, s):
                r = []
                mm.append(r)
                for jj in range(0,s):
                    y = int(i*s + ii)
                    x = int(j*s + jj)
                    #print(x,y)
                    r.append(m[y][x])
                    
    return gg

def flatten(m):
    s = len(m[0][0])
    gg = [[] for i in range(0, s*len(m))]
    rc = 0
    for r in m:
        for c in r:
            for i in range(0, len(c)):
                gg[rc+i] += c[i]
        rc += s   
    
    return gg

def iterate(inp, rulebook, iterations):
    for n in range(0,iterations):
        grid = split(inp, 2 if len(inp)%2 == 0 else 3)
        gg = []
        for r in grid:
            row = []
            gg.append(row)
            for m in r:
                key = mstr(m,'|')
                rule = rulebook.get(key)
                if not rule:
                    raise Exception('(Step %d)No rule for: %s'%(n,key))
                row.append(rule.out)
        
        inp = flatten(gg)
        print('At iteration', n,'size is', len(inp))
    count = 0
    for r in inp:
        for c in r:
            if c == '#':
                count += 1
    return count
mx = ['12','34']#,'789']
print('\n'.join(mx))
print()
print(mstr(rotate_mx(mx, math.pi/2)))
print()
print(mstr(rotate_mx(mx, math.pi)))
print()
print(mstr(rotate_mx(mx, -math.pi/2)))

print('---------')
print(mstr(fliph([['1','2'],['3','4']]),'|'))
print()
print(mstr(flipv([['1','2'],['3','4']])))

print('---------')
print(mstr(fliph([['1','2','3'],['4','5','6'],['7','8','9']])))
print()
print(mstr(flipv([['1','2','3'],['4','5','6'],['7','8','9']])))


inp = [['.','#','.'],['.','.','#'],['#','#','#']]
print('Input pattern:\n%s'%mstr(inp))

import sys

rulebook = get_rulebook(read_input('test_input' if 'test' in sys.argv else 'input'))
print('Rulebook has %d rules'%len(rulebook))

sp = split([[c for c in r] for r in '#..#|....|....|#..#'.split('|')],2)
print(sp)
print(flatten(sp))

print('Part 1:', iterate(inp, rulebook, 5))
print('Part 2:', iterate(inp, rulebook, 18))






