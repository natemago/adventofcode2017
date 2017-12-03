'''

   ---
   \
1 +/   8k       =
   ---
   k e {1,2,..}
   
= 1 + 8 * k(k+1)/2

N = 8k(k+1)/2 + 1
8(k^2 +k)/2 + 1 - N = 0
4k^2 + 4k + 1 - N = 0

   -4 +/- sqrt(16 - 4*4*(1-N))   -4 +/- sqrt(16 + 16 *(N - 1))    -4 +/ sqrt(16*N)  -4 +/- 4*sqrt(N)    1 +/- sqrt(N)
k= ------------------------- = ------------------------------- =   -------------- = ---------------- = --------------
          8                               8                              8                 8                2


solution (1-sqrt(N)) has no meaning in this context

thus
            sqrt(N) + 1
k = ceil ( ------------- ) - 1
                  2


 '''
import math

def get_k(n):
    if n <= 1:
        return 0
    return math.ceil( (math.sqrt(n) + 1) / 2 ) - 1

def total_of(k):
    return 1 + 4 * k * (k + 1)

def dist_l(n, k):
    t = total_of(k-1)
    d = n - t
    print('  d=', d)
    s = 2*k
    d = d%s
    print('  s=',s,', d=',d)
    if d <= k:
        return k-d
    return d-k
    
def p1_get_dist(n):
    if n <= 1:
        return 0
    print(' n =', n)
    k = get_k(n)
    print(' k=', k)
    l = dist_l(n, k)
    print(' l=', l)
    return k  + l
    

# part 2
class Mem:
    def __init__(self, k):
        self.c = (k,k)
        self.k = k
        self.mem = [[0 for j in range(0, 2*k+1)] for i in range(0, 2*k+1)]
        self.mem[k][k] = 1
    
    def __str__(self):
        s = ''
        for row in self.mem:
            for cell in row:
                s += '%8d'%cell
            s += '\n'
        return s
        
    def __repr__(self):
        return self.__str__()
    
    
    def sum_adj(self,r,c):
        s = 0
        if c + 1 < len(self.mem[0]):
            s += self.mem[r][c+1] # right
            if r - 1 >= 0:
                s += self.mem[r-1][c+1] # up-right
            if r + 1 < len(self.mem):
                s += self.mem[r+1][c+1] # down-right
        
        if c - 1 >= 0:
            s += self.mem[r][c-1] # left
            if r - 1 >= 0:
                s += self.mem[r-1][c-1] # up-left
            if r + 1 < len(self.mem):
                s += self.mem[r+1][c-1] # down-left
        
        if r - 1 >= 0:
            s += self.mem[r-1][c] # up
        if r + 1 < len(self.mem):
            s += self.mem[r+1][c] # down
        
        return s
    
    def p2_allocate(self, target):
        r, c = self.c
        c = c + 1 # move right first
        dirs = [
            [-1,0], # up
            [0, -1], # left
            [1, 0], # down
            [0, 1] # right
            ]
        for k in range(1, self.k+1):
            step = 2*k
            for i in range(0,4):
                d = dirs[i]
                for j in range(0, step-1 if not i else step+1 if i==3 else step):
                    s = self.sum_adj(r,c)
                    if s > target:
                        return s
                    self.mem[r][c] = s
                    r,c = r+d[0],c+d[1]
        return None

  
print('Part 1: 312051 -> ', p1_get_dist(312051))

m = Mem(4)

print('Part 2: %d > 312051' % m.p2_allocate(312051))


 