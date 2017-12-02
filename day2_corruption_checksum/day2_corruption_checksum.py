checksum = 0
p2_checksum = 0
with open('input') as inpf:
    for row in inpf:
        row = [int(i) for i in row.strip().split('\t')]
        checksum += max(row) - min(row)
        srow = [i for i in sorted(row, reverse=True)]
        for i in range(0, len(srow)-1):
            for j in range(i+1, len(srow)):
                if srow[i]%srow[j] == 0:
                    p2_checksum += srow[i]//srow[j]

print('Part 1 checksum:', checksum)
print('Part 2 checksum:', p2_checksum)
        
        