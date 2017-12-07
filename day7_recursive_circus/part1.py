import re
from collections import namedtuple

class Program:
    def __init__(self, name, weight=None, subprogs=None, parent=None):
        self.name = name
        self.weight = weight
        self.subprogs = subprogs
        self.parent = parent
        self._total_weight = None
        
    def total_weight(self, tower):
        if self._total_weight is not None:
            return self._total_weight
        w = self.weight
        for s in self.subprogs:
            w += tower[s].weght(tower)
        self._total_weight = w
        return w
    
    def __str__(self):
        subs = ' -> %s'%','.join(self.subprogs) if len(self.subprogs) else ''
        parent = self.parent.name if self.parent else '<Root>'
        return '%s (%d) [%s]%s'%(self.name, self.weight, parent, subs)

#Program = namedtuple('Program', ['name','weight','subrogs','parent'])

tower = {}

with open('input') as inpf:
    for line in inpf:
        m = re.match('(?P<name>\\w+) \\((?P<weight>\\d+)\\).*', line)
        if not m:
            raise Exception('Wrong regex: ', line)
        name = m.group('name')
        weight = int(m.group('weight'))
        subprogs = []
        #print(line)
        #print('  ', name)
        #print('  ', weight)
        if '->' in line:
            subprogs = [n.strip() for n in line.split('->')[1].strip().split(',')]
            #print('  ', subprogs)
        
        prog = Program(name=name, weight=weight, subprogs=subprogs, parent=None)
        if tower.get(name):
            prog.parent = tower[name].parent
            
        tower[name]=prog
        
        for sub in subprogs:
            sp = tower.get(sub)
            if sp:
                sp.parent = prog
            else:
                sp = Program(name=sub, parent=prog)
                tower[sub] = sp

def find_root(tower):
    root = None
    for _, prog in tower.items():
        if prog.parent is None:
            if root is not None:
                raise Exception('Opps, more than one root:',  root, prog)
            root = prog
    return root


def balance_the_tower(tower):
    root = find_root(tower)
    
    def ballance(prog, tower):
        if len(prog.subprogs) in [0, 1]:
            return None
        if len(prog.subprogs) == 2:
            if tower[prog.subprogs[0]).total_weight() != tower[prog.subprogs[1]].total_weight():
                raise Exception('Now this is a cunandrom: The 2 subtowers have different weight. Which one is correct? %s'%prog)
        first = (prog.subprogs[0], tower[prog.subprogs[0]].total_weight())
        next = None
        for subname in prog.subprogs:
            sub = tower[subname]
            if tower[sub].total_weight() != first[1]:
                if next is not None:
                    print('Found it')
                

print('Part 1: The root program is', find_root(tower))


