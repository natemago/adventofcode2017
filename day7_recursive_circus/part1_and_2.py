import re
from collections import namedtuple

class Program:
    def __init__(self, name, weight=None, subprogs=None, parent=None):
        self.name = name
        self.weight = weight
        self.subprogs = subprogs
        self.parent = parent
        self._total_weight = None

    def total_weight(self):
        if self._total_weight is not None:
            return self._total_weight
        w = self.weight
        for s in self.subprogs:
            w += s.total_weight()
        self._total_weight = w
        return w

    def __str__(self):
        subs = ' -> %s'%','.join([p.name for p in self.subprogs]) if len(self.subprogs) else ''
        parent = self.parent.name if self.parent else '<Root>'
        return '%s (%d) [%s]%s'%(self.name, self.weight, parent, subs)

    def is_leaf(self):
        return len(self.subprogs) == 0

    def get_unballanced(self):
        unb = None
        prev = None
        for s in self.subprogs:
            if prev is None:
                prev = s
                continue
            if s.total_weight() != prev.total_weight():
                unb = prev
                if s == self.subprogs[-1]:
                    unb = s
        return unb

tower = {}

with open('input') as inpf:
    for line in inpf:
        m = re.match('(?P<name>\\w+) \\((?P<weight>\\d+)\\).*', line)
        if not m:
            raise Exception('Wrong regex: ', line)
        name = m.group('name')
        weight = int(m.group('weight'))
        subprogs = []
        if '->' in line:
            subprogs = [n.strip() for n in line.split('->')[1].strip().split(',')]
        prog = Program(name=name, weight=weight, subprogs=[], parent=None)
        if tower.get(name):
            prog = tower[name]
            prog.weight = weight

        tower[name]=prog
        sbs = []
        for sub in subprogs:
            sp = tower.get(sub)
            if sp:
                sp.parent = prog
            else:
                sp = Program(name=sub, parent=prog, subprogs=[], weight=0)
                tower[sub] = sp
            sbs.append(sp)
        prog.subprogs = sbs

def find_root(tower):
    root = None
    for _, prog in tower.items():
        if prog.parent is None:
            if root is not None:
                raise Exception('Opps, more than one root:',  root, prog)
            root = prog
    return root


def ballance(tower):
    root = find_root(tower)

    def ballance_p(prog):
        # check if we hit a leaf, we don't check if leafs are ballanced (they are).
        if prog.is_leaf():
            return None
        # Dig in depth-first, we need to get the deepest unballanced node to balance it.
        for sp in prog.subprogs:
            u = ballance_p(sp)
            if u:
                return u
        unb = prog.get_unballanced()
        if unb is not None:
            print('Unballanced: ', unb, ' with total weight: ', unb.total_weight())
            return unb
        return None

    unb = ballance_p(root)
    if unb:
        if unb.parent:
            for p in unb.parent.subprogs:
                if p != unb:
                    d = p.total_weight() - unb.total_weight()
                    return unb.weight + d
    return None

print('Part 1: The root program is', find_root(tower))
print('Part 2: Ballance: ', ballance(tower))
