def read_input(inpf):
    with open(inpf) as f:
        return [int(i.strip()) for i in f.read().strip().split(',')]

class KnotString:
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

inp = read_input('input')
print('Input:', inp)
tks = KnotString(size=5, lengths=[3,4,1,5])
tks.reverse_all()
print('Test: ', tks.string)



p1 = KnotString(size=256, lengths=inp)
p1.reverse_all()
print('Part1:', p1.string[0]*p1.string[1])
