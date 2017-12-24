#from collections import namedtuple

#Comp = namedtuple('Comp', ['a','b','chain', 'sum', 'rem'])

class Comp:
    def __init__(self, a, b, chain=None, sum=None, rem=None,conn=None):
        self.a = a
        self.b = b
        self.chain= chain
        self.sum = sum
        self.rem = rem
        self.conn = conn
        
    def __repr__(self):
        return '%d/%d [%d]'%(self.a, self.b, self.sum)
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, o):
        if isinstance(o, Comp):
            return self.a == o.a and self.b == o.b
        return False
    
    def __hash__(self):
        return (self.a, self.b).__hash__()

def read_input(f):
    components = []
    with open(f) as inpf:
        for line in inpf:
            ab = line.strip().split('/')
            c = Comp(a=int(ab[0]),b=int(ab[1]), sum=0)
            components.append(c)
    cset = set(components)
    cc = {}
    for c in components:
        c.chain = set()
        c.rem = cset - {c}
        k1 = '%d-%d'%(c.a,c.b)
        k2 = '%d-%d'%(c.b,c.a)
        if cc.get(k1):
            print('woops', k1)
        if cc.get(k2):
            print('woops', k2)
            
    return components

def bridge(comp, i):
    max_w = comp.sum
    max_c = None
    #print('B:', comp, 'is connected on', comp.conn)
    if comp.conn is None:
        print('nope, error')
        return
    for c in comp.rem:
        can_connect = False
        
        if comp.conn == 'a':
            if comp.b == c.a:
                can_connect = 'a'
            elif comp.b == c.b:
                can_connect = 'b'
        else:
            if comp.a == c.a:
                can_connect = 'a'
            elif comp.a == c.b:
                can_connect = 'b'   
                        
        if can_connect:
            nc = Comp(a=c.a, b=c.b, chain=comp.chain.union({c}), sum=comp.sum+c.a+c.b, rem=comp.rem-set({c}), conn=can_connect)
            weight = bridge(nc, i+1)
            if max_w < weight:
                max_w = weight
                max_c = nc
    return max_w



def longest_strongest_bridge(comp, i):
    max_w = comp.sum
    max_l = i
    if comp.conn is None:
        print('nope, error')
        return
    for c in comp.rem:
        can_connect = False
        
        if comp.conn == 'a':
            if comp.b == c.a:
                can_connect = 'a'
            elif comp.b == c.b:
                can_connect = 'b'
        else:
            if comp.a == c.a:
                can_connect = 'a'
            elif comp.a == c.b:
                can_connect = 'b'   
                        
        if can_connect:
            nc = Comp(a=c.a, b=c.b, chain=comp.chain.union({c}), sum=comp.sum+c.a+c.b, rem=comp.rem-set({c}), conn=can_connect)
            weight, length = longest_strongest_bridge(nc, i+1)
            if length >= max_l:
                if length > max_l:
                    max_w = weight
                    max_l = length
                elif weight >= max_w:
                    max_w = weight
                    max_l = length
    return max_w, max_l


def part1(components):
    max_w = None
    
    for c in components:
        is_start = False
        if c.a == 0:
            is_start = 'a'
        elif c.b == 0:
            is_start = 'b'
        
        if is_start:
            c.conn = is_start
            c.sum = c.a+c.b
            weight = bridge(c, 1)
            if max_w is None or weight > max_w:
                max_w = weight
    return max_w


def part2(components):
    max_w = None
    max_l = 1
    
    for c in components:
        is_start = False
        if c.a == 0:
            is_start = 'a'
        elif c.b == 0:
            is_start = 'b'
        
        if is_start:
            c.conn = is_start
            c.sum = c.a+c.b
            weight,length = longest_strongest_bridge(c, 1)
            if length >= max_l:
                if length > max_l:
                    max_l = length
                    max_w = weight
                elif max_w is None or weight >= max_w:
                    max_l = length
                    max_w = weight
    return max_l, max_w


import sys

if 'test' in sys.argv:
    print('Test (p1):', part1(read_input('test_input')))
    print('Test (p2):', part2(read_input('test_input')))

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))
