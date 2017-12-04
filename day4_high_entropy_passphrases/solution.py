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
            for anagram in itertools.permutations(word, len(word)):
                anagram = ''.join(anagram)
                if anagram == word:
                    continue
                if passphrases.get(anagram):
                    return False
    return True


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
