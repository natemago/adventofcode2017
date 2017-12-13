def read_input(inf):
    firewall = []
    with open(inf) as inpf:
        for line in inpf:
            parts = line.split(': ')
            firewall.append( ( int(parts[0].strip()), int(parts[1].strip()) ) )
    return firewall

def trip_severity(firewall, wait=0):
    severity = 0
    caught = False
    for layer, depth in firewall:
        if (layer+wait) % (2*(depth - 1)) == 0:
            severity += layer*depth
            caught = True
    return (severity, caught)

def wait_time(firewall):
    wait = 0
    while  True:
        _, got_caught = trip_severity(firewall, wait)
        if not got_caught:
            return wait
        wait += 1


print('Part 1: Trip severity: ', trip_severity(read_input('input'))[0])
print('Part 2: Wait time: ', wait_time(read_input('input')))
