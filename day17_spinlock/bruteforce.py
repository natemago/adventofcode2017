def evolve_spinlock(n, lim):
    buff = [0]
    p = 0
    for i in range(1, lim):
        p = (p+n+1)%len(buff)
        buff = buff[0:p+1] + [i] + buff[p+1:]
        
    return buff

def evolve_spinlock_p2(n, lim):
    p = 0
    val = None
    for i in range(1, lim):
        p = (p+n+1)%i
        if p == 0: # we insert right after p
            val = i
    return val


buff = evolve_spinlock(303, 2018)
print('Part 1:', buff[buff.index(2017) + 1])
value = evolve_spinlock_p2(303, 50000000)
print('Part 2:', value)