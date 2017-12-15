

#prevA = 65
#prevB = 8921

def part1(a, b):
    prevA = a
    prevB = b
    count = 0
    for i in range(0, 40000000):
        #print(prevA, prevB)
        nextA = ((prevA*16807)%2147483647)
        nextB = ((prevB*48271)%2147483647)
        if  (nextA & 0xFFFF) == (nextB & 0xFFFF):
            count += 1
        prevA = nextA
        prevB = nextB
    return count

def part2(a, b):
    count = 0
    n = 5000000
    for i in range(0, 5000000):
        ga = None
        while True:
            nextA = (a*16807)%2147483647
            a = nextA
            if nextA % 4 == 0:
                ga = nextA
                break
        gb = None
        while True:
            nextB = (b*48271)%2147483647
            b = nextB
            if nextB % 8 == 0:
                gb = nextB
                break

        if (ga & 0xFFFF) == (gb & 0xFFFF):
            count += 1
    return count


print('Part 1: ', part1(634, 301))
print('Part 2: ', part2(634, 301))
