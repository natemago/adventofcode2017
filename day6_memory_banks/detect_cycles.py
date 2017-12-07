import re

def read_input(inp_name):
    with open(inp_name) as inpf:
        return [int(i) for i in re.findall('\\d+', inpf.read())]

print(read_input('input'))

def detect_cycle(mem_banks):
    cycles = 0
    seen = {}
    while True:
        sig = '|'.join([str(i) for i in mem_banks])
        #print(sig)
        if seen.get(sig) is not None:
            return (cycles, seen[sig], cycles-seen[sig])
        seen[sig] = cycles
        cycles += 1
        max_idx = mem_banks.index(max(mem_banks))
        mx = mem_banks[max_idx]
        mem_banks[max_idx] = 0
        for i in range(1, mx+1):
            mem_banks[(max_idx+i)%len(mem_banks)] += 1
    return cycles

print('Test case: Cycle detected at %d (starting at %d) with length %d.' % detect_cycle([0,2,7,0]))
print('Part 1 and 2: Cycle detected at %d (starting at %d) with length %d.' % detect_cycle(read_input('input')))
