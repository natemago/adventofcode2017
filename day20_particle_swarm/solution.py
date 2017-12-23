'''
t   x
--+---
0   x   = 3 (v=2,a=-1)
1   x + v + a = 3 + 2 - 1 = 4 
2   x + v + a + v + a + a = 3 + 2 - 1 + 2 - 1 - 1 = 4
3   x + v + a + v + a + a + v + a + a + a = 3 + 2 -1 + 2 - 1 - 1 + 2 - 1 - 1 - 1 = 3
4   x + v + a + v + a + a + v + a + a + a + v + 4a
.
.
.
n   x + n*v + a + 2*a + 3*a + ... n*a

--------------------------------------------

S(n) = x + n*v + n(n+1)a/2

============================

S(n, p1) = x1 + n*v1 + n(n+1)a1/2
S(n, p2) = -//-

S(n, p1) = S(n, p2)
x1 + n*v1 + n(n+1)a1/2 = x2 + n*v2 + n(n+1)a2/a

x1-x2 + n(v1-v2) + n(n+1)*(a1-a2)/2 = 0

============================

X = x1-x2
V = v1-v2
A = a1-a2/2


X + n*V + n(n+1)A = 0

X + n*V + A*n^2 + A*n = 0
A*n^2 + (V+A)*n + X = 0


    -(V+A) +/- sqrt((V+A)^2 - 4*A*X)
n = ----------------------------------
            2*A

No solutions (no collision) if:
 * (V+A)^2 - 4*A*X < 0
 * if A == 0 and V == 0 and X != 0


When A = 0 (same acceleration)
==============================

(V+A)*n + X = 0
V*n + X = 0

     -X
n = ------- 
      V

no collision if:
   V = 0 (same speed)

Edge cases
=======================
 - in tick 0, if the points ar at the same position, - remove them (collision) ?



re.findall('(p|a|v)=<([\\d,]+)>','p=<1,2,3>, v=<12,34,56>, a=<123,3>')

'''



import re
import math


class Particle:
    def __init__(self, n, p=None, v=None, a=None):
        self.n = n
        self.p = p
        self.a = a
        self.v = v
        self.collisions = []
    
    def __repr__(self):
        return 'P(%d)'%self.n
    
    def __str__(self):
        return self.__repr__()
    
    def p_at(self, n):
        def cx(i, n):
            return (n*(n+1)/2)*self.a[i] + n*self.v[i] + self.p[i]
        return [cx(0, n), cx(1,n), cx(2,n) ]
        
    def collides(self, op):
        coll_times = []
        if self.p == op.p:
            return [0]
        for ax in range(0,3):
            coll_times.append([])
            X = self.p[ax] - op.p[ax]
            V = self.v[ax] - op.v[ax]
            A = (self.a[ax] - op.a[ax])/2
            
            if A == 0:
                if V == 0:
                    if X == 0:
                        # special case, the particles are at the same spot - collide at every tick on this axis
                        coll_times[ax].append(-1)
                        continue
                    else:
                        return None 
                n = -X/V
                if n > 0:
                    coll_times[ax].append(n)
                    continue
                return None
                
            if (V+A)**2 - 4*A*X < 0:
                return None
            n1 = solve(1, A, (V+A), X)
            n2 = solve(-1, A, (V+A), X)
            #print(n1,n2)
            
            if n1 > 0:
                coll_times[ax].append(n1)
            if n2 > 0:
                coll_times[ax].append(n2)
            if len(coll_times[ax]) == 0:
                return None
        #print(coll_times)
        return collision_times(coll_times)


def collision_times(ct):
    Sn = set()
    
    for i in range(0,3): # axis
        for v in ct[i]: # value
            if (v in ct[(i+1)%3] or -1 in ct[(i+1)%3]) and (v in ct[(i+2)%3] or -1 in ct[(i+2)%3]):
                Sn.add(v)
    if len(Sn) == 0:
        return None
    return list(Sn)


def solve(i, a, b, c):
   return (-b +i*math.sqrt(b**2-4*a*c) )/(2*a)               

def load_input(f):
    c=0
    particles = []
    with open(f) as inpf:
        for ln in inpf:
            specs = re.findall('(p|a|v)=<([-\\d,]+)>', ln.strip())
            #print(specs)
            particle = Particle(n=c)
            for s in specs:
                vals = [int(i.strip()) for i in s[1].split(',')]
                
                if s[0] == 'p':
                    particle.p = vals
                elif s[0] == 'v':
                    particle.v = vals
                else:
                    particle.a = vals
            
            particles.append(particle)
            c+=1
    return particles

def part2(particles):
    for i in range(0, len(particles)-1):
        for j in range(i+1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            Sn = p1.collides(p2)
            if Sn:
                #print(p1,'with',p2,'at',Sn)
                for s in Sn:
                    
                    if (len(p1.collisions)==0 or s <= p1.collisions[0][0]) and (len(p2.collisions)==0 or s <= p2.collisions[0][0]):
                        # this collision must be valid for both particles, but we must prune the other collisions as well
                        #s = int(s)
                        if len(p1.collisions):
                            prune_collisions(p1, s)
                        if len(p2.collisions):
                            prune_collisions(p2, s)
                            
                        p1.collisions.append((s, p2))
                        p2.collisions.append((s, p1))
                    
                        p1.collisions = [i for i in sorted(p1.collisions, key=lambda x: x[0])]
                        p2.collisions = [i for i in sorted(p2.collisions, key=lambda x: x[0])]
   
    count = 0
    for p in particles:
        #print(p, p.collisions)
        if len(p.collisions):
            count+=1
    return count, len(particles), len(particles) - count            

def prune_collisions(p, col):
    prune = []
    for c in p.collisions:
        if c[0] > col:
            prune.append(c)
    
    for pr in prune:
        p.collisions.remove(pr)
        opr = []
        for c in pr[1].collisions:
            if c[1] == p:
                opr.append(c)
        
        for c in opr:
            pr[1].collisions.remove(c)    

import sys

particles = load_input('test_inp' if 'test' in sys.argv else 'input')
print(len(particles),'particles')
print('Part 1:', sorted( sorted(particles, key=lambda p: [abs(i) for i in p.p]), key=lambda p: [abs(i) for i in p.a])[0])
print('Part 2: %d collisions of %d total particles. %d particles left after all colisions resolved.' % part2(particles))
#print(particles[138].collides(particles[54]))

#for i in range(0, 5):
#    print('Tick: ', i)
#    for p in particles:
#        print(p, p.p_at(i))
#    print('--------')


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        