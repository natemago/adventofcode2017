from PIL import Image, ImageDraw

def move_odd_even(v, odd, even):
    return even if abs(v) % 2 == 0 else odd

MOVES = {
    'n':  [0, -1],
    'nw': [-0.866, -0.5],
    'ne': [0.866, -0.5],
    'sw': [-0.866, 0.5],
    's':  [0, 1],
    'se': [0.866, 0.5]
}


pallete = {
    'n': (0,0,255),
    'ne': (0,255,255),
    'nw': (255,0,255),
    's': (255,128,0),
    'se': (128,255,0),
    'sw': (255,255,0)
}


def read_input(fn):
    with open(fn) as inpf:
        return [m.strip().lower() for m in inpf.read().strip().split(',')]

def walk(moves, imgfile, imgsize, scale, trans):
    img = Image.new('RGB', imgsize)
    draw = ImageDraw.Draw(img)
    w = trans[0]*imgsize[0]
    h = trans[1]*imgsize[1]
    x = 0
    y = 0
    max_steps = 0
    last_steps = 0
    draw.text((w,h), 'START', fill=(0,255,0))
    for move in moves:
        if not move:
            raise Exception('Woops, dirty input - empty move')
        dv = MOVES.get(move)
        if not dv:
            raise Exception('Unknown move: %s'%move)
        px,py = x,y
        x += dv[0]
        y += dv[1]
        draw.line(((px*scale+w,py*scale+h), (x*scale+w,y*scale+h)), fill=pallete[move])
        print(x,y)
    
    draw.text((x*scale+w,y*scale+h), 'END', fill=(255,0,0))
    
    lx = 30
    ly = 30
    
    for d, color in pallete.items():
        draw.text((lx, ly), text=d, fill=color)
        draw.line(((lx+15, ly+6), (lx+20, ly+6)), width=2, fill=color)
        ly+=15
        
    
    with open(imgfile, mode='wb') as imgout:
        img.save(imgout, 'PNG')


walk(read_input('input'),'out.png', (1080,1920), 1, (0.74, 0.7))
