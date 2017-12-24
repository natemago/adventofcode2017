import math


def is_prime(n):
    i = 2
    sq = math.sqrt(n)
    
    while i <= sq:
        if n%i == 0:
            return False
        i+=1
    
    return True


count = 0

b = 67*100+100000
c = b + 17000

while b <= c:
    if not is_prime(b):
        count+=1
    b += 17
print(count)