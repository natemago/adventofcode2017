set b 67
set c b
jnz a 2 to label_1
jnz 1 5 to label 2
mul b 100 :label_1
sub b -100000 
set c b
sub c -17000
set f 1 :label_2:
set d 2
set e 2 :label_5
set g d :label_4
mul g e
sub g b
jnz g 2 to label_3
set f 0
sub e -1 :label_3
set g e
sub g b 
jnz g -8 to label_4
sub d -1
set g d
sub g b
jnz g -13 to label_5
jnz f 2 to label_6
sub h -1 
set g b :label_6
sub g c
jnz g 2 to label_7
jnz 1 3 :HALT
sub b -17 :label_7
jnz 1 -23 to label_2
