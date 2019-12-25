import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Arrow
from math import sin, cos
from random import randint, random, choice

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
#patch = plt.Circle((5, -5), 0.75, fc='y')
patch = Circle((5, -5), 0.75, fc='y')
arr = Arrow(0,0,1,1)

total_pts = 4
pts = np.zeros(total_pts,
    dtype=[ ('x', float, (1,)),
        ('y',float,(1,)),
])

directions = np.zeros(total_pts)
coffi = np.zeros(total_pts)

for i in range(1,len(pts)):
    coffi[i] = 1 + 2*random()
    directions[i] = choice([1,-1])


length = 2

print(pts['x'])

line, = ax.plot([],[], 'o-', lw=3)

def init():
    line.set_data([],[])
    return line,

def animate(i):
    rad = i*0.1
    pts[0] = 3,3
    for i in range(1,len(pts)):
        x,y = pts[i-1]
        pts[i] = x+directions[i]*cos(rad*coffi[i]), y+directions[i]*sin(rad*coffi[i])
    line.set_data( pts['x'], pts['y'])
    return line,


anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()