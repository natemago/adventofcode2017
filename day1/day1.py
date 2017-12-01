def solve_captcha_p1(captcha):
    captcha_sum = 0
    for i in range(0, len(captcha)):
        next_digit = captcha[(i+1)%len(captcha)]
        if captcha[i] == next_digit:
            captcha_sum += int(next_digit)
    return captcha_sum

def solve_captcha_p2(captcha):
    captcha_sum = 0
    for i in range(0, len(captcha)):
        next_digit = captcha[(i + (len(captcha)//2))%len(captcha)]
        if captcha[i] == next_digit:
            captcha_sum += int(next_digit)
    return captcha_sum

captcha = ''
with open('input') as inp:
    captcha  =inp.read()
    captcha = captcha.strip()

print('== Part 1==')
print('1122=',solve_captcha_p1('1122'))
print('1111=',solve_captcha_p1('1111'))
print('1234=',solve_captcha_p1('1234'))
print('91212129=',solve_captcha_p1('91212129'))
print('Part 1 solution:', solve_captcha_p1(captcha))

print('')

print('== Part 2 ==')
print('1212=',solve_captcha_p2('1212'))
print('1221=',solve_captcha_p2('1221'))
print('123425=',solve_captcha_p2('123425'))
print('123123=',solve_captcha_p2('123123'))
print('12131415=',solve_captcha_p2('12131415'))
print('Part 2 solution: ', solve_captcha_p2(captcha))
