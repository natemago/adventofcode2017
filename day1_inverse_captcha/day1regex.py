import re
cpt=''
with open('input') as inp:
  cpt = inp.read().strip()

# part 1
print(sum([int(i) for i in re.findall('(.)(?=\\1)', cpt+cpt[0])]))

# part 2
print(sum([int(i) for i in re.findall('(\\d)(?=.{%d}\\1)'%(len(cpt)//2-1), cpt+cpt[0:len(cpt)//2])]))
