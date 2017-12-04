import re
import itertools


def is_valid(passphrase, check_anagrams=False):
    passphrase = passphrase.strip()
    passphrases = {}
    for word in re.findall('\\w+', passphrase):
        if passphrases.get(word):
            return False
        passphrases[word] = 1
        if check_anagrams:
            ws = word_signature(word)
            if passphrases.get(ws):
                return False
            passphrases[ws] = 1
    return True

def word_signature(word):
    sig = {}
    for l in word:
        if not sig.get(l):
            sig[l] = 1
        else:
            sig[l] += 1

    letters = sorted([k for k,_ in sig.items()])
    return ''.join(['%s%d'%(l, sig[l]) for l in letters])

def count_valid(lines, check_anagrams=False):
    valid = 0
    for line in lines:
        if is_valid(line, check_anagrams):
            valid+=1
    return valid

lines = []
with open('input') as inpf:
    for line in inpf:
        lines.append(line.strip())

print('Part 1. Valid passphrases count: ', count_valid(lines))
print('Part 2. Valid passphrases (extra security) count:', count_valid(lines, True))
