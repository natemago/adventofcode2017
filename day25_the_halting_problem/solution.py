class TuringMachine:
    def __init__(self, table, tape=None, state=None,cursor=None):
        self.table = table
        self.tape = tape or []
        self.state = state
        self.cursor = cursor or 0
        if len(self.tape) <= self.cursor:
            for i in range(0, len(self.tape) - self.cursor + 1):
                self.tape.append(0)
   
    def next(self):
        rule = self.table[self.state]
        val = self.tape[self.cursor]
        write, move, state = rule[val]
        
        if move == 1: # right
            if len(self.tape) <= self.cursor + 2:
                self.tape.append(0)
            self.tape[self.cursor] = write
            self.cursor += 1
        elif move == -1: # left
            self.tape[self.cursor] = write
            if self.cursor == 0:
                self.tape = [0] + self.tape
            else:
                self.cursor -= 1
        else: # don't move
            self.tape[self.cursor] = write
        
        self.state = state
    


def part1():
    table = {
        'A': [(1, 1, 'B'),(0, 1, 'C')],
        'B': [(0, -1, 'A'),(0, 1, 'D')],
        'C': [(1, 1, 'D'),(1, 1, 'A')],
        'D': [(1, -1, 'E'),(0, -1, 'D')],
        'E': [(1, 1, 'F'),(1, -1, 'B')],
        'F': [(1, 1, 'A'),(1, 1, 'E')]
    }
    tm = TuringMachine(table=table, cursor=0, state='A')
    
    for i in range(0, 12368930):
        tm.next()
        if i % 1000 == 0:
            print(i)
    print('done')
    return sum(tm.tape)
    
print('Part1 :', part1())