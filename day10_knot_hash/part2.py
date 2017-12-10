def read_input(inpf):
    with open(inpf) as f:
        return [ord(c) for c in f.read().strip()] + [17, 31, 73, 47, 23]

def test_inp(s):
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
        return ''.join(['{:02X}'.format(x) for x in hsh]).lower()
        #return hsh

inp = read_input('input')
print('Input:', inp)
tks = KnotStringHash(size=256, lengths=inp) #test_inp('1,2,4'))
print('Part 2: ', tks.knot_hash())
