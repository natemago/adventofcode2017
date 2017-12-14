def read_input(inpf):
    with open(inpf) as f:
        return [ord(c) for c in f.read().strip()] + [17, 31, 73, 47, 23]

def str_inp(s):
    return [b for b in s.encode('ascii')] + [17, 31, 73, 47, 23]

class KnotStringHash:
    def __init__(self, size, lengths):
        self.size = size
        self.string = [i for i in range(0, size)]
        self.lengths = lengths
        self.pos = 0
        self.skip = 0

    def sublist(self, length):
        lst = []
        for i in range(0, length):
            lst.append(self.string[(self.pos+i)%self.size])
        return lst

    def override(self, lst, at_post):
        for i in range(0, len(lst)):
            self.string[(i+self.pos)%self.size] = lst[i]

    def reverse_next(self, length):
        sublst = [i for i in reversed(self.sublist(length))]
        self.override(sublst, self.pos)
        self.pos = (self.pos + length + self.skip)%self.size
        self.skip += 1

    def reverse_all(self):
        for l in self.lengths:
            self.reverse_next(l)

    def knot_hash(self):
        for i in range(0, 64):
            self.reverse_all()
        hsh = []
        for i in range(0, 16):
            block = 0
            for j in range(0, 16):
                block ^= self.string[i*16+j]
            hsh.append(block)
        #return ''.join(['{:02X}'.format(x) for x in hsh]).lower()
        return hsh


def to_binary(n):
    ba = []
    for _ in range(0,8):
        ba.append(n&0x1)
        n = n//2
    return ba

def bin_sum(arr):
    s = 0
    a = []
    for i in arr:
        bi = to_binary(i)
        s += sum(bi)
        a = a + bi
    return (s, a)

INPUT = 'jzgqcdpd'

def get_grid(inp):
    used = 0
    grid = []
    for i in range(0, 128):
        row_used, row = bin_sum(KnotStringHash(256, str_inp('%s-%d'%(inp, i))).knot_hash())
        used += row_used
        grid.append(row)
    return used, grid


def mark_group(grid, pos, group):
    if grid[pos[0]][pos[1]] >= 0:
        return # already marked (>0) or not a group (==0)
    grid[pos[0]][pos[1]] = group

    if pos[0] - 1 >= 0: # up
        mark_group(grid, (pos[0]-1, pos[1]), group)
    if pos[0] + 1 < len(grid): # down
        mark_group(grid, (pos[0]+1, pos[1]), group)
    if pos[1] - 1 >= 0: # left
        mark_group(grid, (pos[0], pos[1]-1), group)
    if pos[1] + 1 < len(grid[0]): # right
        mark_group(grid, (pos[0], pos[1] + 1), group)

def part2_count_groups(grid):
    grd = [[-1 if i else 0 for i in row] for row in grid]

    group = 0
    for y in range(0, len(grd)):
        for x in range(0, len(grd[y])):
            c = grd[y][x]
            if c < 0:
                group += 1
                mark_group(grd, (y,x), group)
    return group

used, grid = get_grid(INPUT)
print('Part 1: Total used ', used)
print('Part 2: Total groups', part2_count_groups(grid))
