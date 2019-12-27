import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Arrow
from math import sin, cos
import math
from random import randint, random, choice
import cmath
import sys
from tqdm import tqdm
total_frames = 1000
pbar = tqdm(total=total_frames)


fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

data = {
    'total_terms': 4,
    -2:8-23j,
    -1:8+9j,
    0:24.346+56j,
    1:4.23-27j,
    2:23,
}

ax = plt.axes(xlim=(-100, 100),  ylim=(-50, 200))

total_pts = data['total_terms']
pts = np.zeros(total_pts+1 ,
    dtype=[ ('x', float, (1,)),
        ('y',float,(1,)),
])


def compute_term(n, coffi, i):
    ''' n : The Nth frequency term
        coffi: coffieicnet for your term
        i : the angle for your circle
    '''
    return coffi * cmath.exp(n*2*math.pi*1j*i)


directions = np.zeros(total_pts)
coffi = np.zeros(total_pts)

# for i in range(1,len(pts)):
    # coffi[i] = 
    # directions[i] = choice([1,-1])

def point_idx_to_term(idx):
    '''
        Convert point indices to the terms it represent.

        idx| 0 |  1 | 2 |  3 | 4 |
        --------------------------
           | 0 | -1 | 1 | -2 | 2 |
    '''
    if idx == 0:
        return 0
    residual = (idx-1) %2
    term_abs = (idx+1) // 2
    term = term_abs * -1 if residual==0 else term_abs
    return term

# length = 2

print(pts['x'])

line, = ax.plot([],[], 'o-', lw=3)

def init():
    line.set_data([],[])
    return line,

def animate(i):
    rad = i*0.002
    pts[0] = 3,3
    for i in range(len(pts)):
        # a complex number
        term = point_idx_to_term(i)
        # print(f'idx:{i} term:{term}')
        # print(f'data[{term}]: {data[term]}')
        coffi = data[term]
        if i==0:
            x,y = 0,0
        else:
            x,y = pts[i-1]
        # print(f'x:{x}, y:{y}')
        # sys.exit()

        next_pos = complex(x,y) + coffi*cmath.exp(term * 2 * math.pi * 1j * rad)
        pts[i] = next_pos.real, next_pos.imag
    line.set_data( pts['x'], pts['y'])
    pbar.update(1)

    return line,

anim = animation.FuncAnimation(fig, animate,
                               init_func=init,
                               frames=total_frames,
                               interval=20,
                               blit=True)
anim.save('good.mp4', writer='ffmpeg')
#plt.show()