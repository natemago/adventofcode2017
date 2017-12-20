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
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		