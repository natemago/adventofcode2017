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


mn = None
c=0
with open('input') as f:
	for ln in f:
		p=ln.strip().split('>, ')
		a=[int(i.strip()) for i in p[2].strip()[3:-1].split(',')]

				

#				print(a)
		#if mn is None:
		s=sum([abs(i) for i in a]) 
		if mn is None:
			mn=(s,a,ln,c)
		if mn[0] >= s:
			mn=(s,a,ln,c)
		c+=1
print(mn)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		