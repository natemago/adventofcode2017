def read_input(ifn):
    with open(ifn) as inpf:
        for line in inpf:
            parts = line.strip().split('<->')
            pid = parts[0].strip()
            neighbours = []
            if len(parts) > 1:
                neighbours = [p.strip() for p in parts[1].strip().split(',')]
            yield (pid, neighbours)

class Node:
    def __init__(self, name, vertices=None, data=None):
        self.name = name
        self.vertices = vertices or []
        self.data = data or {}

class Vertex:
    def __init__(self, nodes, data=None):
        self.nodes = nodes
        self.data = data or {}

class Graph:
    def __init__(self):
        self.nodes = {}
        self.vertices = {}

    def add_node(self, node):
        if self.nodes.get(node.name):
            raise Exception('dupicate node %s'%node.name)
        self.nodes[node.name] = node

    def add_vertex(self, node1, node2):
        n1 = self.nodes[node1]
        n2 = self.nodes[node2]
        vx = Vertex([n1, n2])
        n1.vertices.append(vx)
        n2.vertices.append(vx)
        self.vertices['%s-%s'%(node1, node2)] = vx
        return vx


def load_program_graph(inpf):
    graph = Graph()
    for pid, neighbours in read_input(inpf):
        node = graph.nodes.get(pid)
        if node is None:
            node = Node(pid)
            graph.add_node(node)

        for n in neighbours:
            nnode = graph.nodes.get(n)
            if not nnode:
                nnode = Node(n)
                graph.add_node(nnode)
            graph.add_vertex(node.name, n)
            graph.add_vertex(n, node.name)
    return graph

def part1_count_group_zero(graph):
    n = graph.nodes['0']

    def mark(node):
        if node.data.get('mark'):
            return
        node.data['mark'] = True
        for v in node.vertices:
            mark(v.nodes[1])

    mark(n)
    count = 0
    for _, n in graph.nodes.items():
        if n.data.get('mark'):
            count+=1
    return count

def part2_count_groups(graph):
    def mark_group(n, grp):
        if n.data.get('group'):
            return # already marked
        n.data['group'] = grp
        for v in n.vertices:
            if v.nodes[0] != n:
                mark_group(v.nodes[0], grp)
            if v.nodes[1] != n:
                mark_group(v.nodes[1], grp)
    group = 0
    for _, node in graph.nodes.items():
        if node.data.get('group') is None:
            group += 1
            mark_group(node, group)
    return group

graph = load_program_graph('input')

print('Part1: Group zero size: ', part1_count_group_zero(graph))
print('Part2: Total number of groups: ', part2_count_groups(graph))
