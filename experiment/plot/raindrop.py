import numpy as np
import matplotlib

import matplotlib.animation as animation
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
from random import randint, random
from tqdm import tqdm

def rand_pos(low=0, high=100):
    return ( randint(low,high), randint(low,high))

def random_color():
    return (random(),random(),random())

class Vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end



class Raindrop:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10
        self.alpha = 1
        self.color = random_color()
        self.circle = Circle(self.pos,self.radius,linewidth=3, color=self.color, fill=False, alpha=self.alpha)
        self.restart = False

    def __repr__(self):
        return f"<Raindrop pos:{self.pos}, radius:{self.radius}>"
    def tick(self):
        if self.restart == True:
            self.radius = 0
            self.alpha = 1
            self.pos = rand_pos(-200,200)
            self.restart = False
        
        self.radius += 1
        # if self.alpha >= 0.1:
        #     self.alpha -= 1/(self.radius)
        self.alpha = min(1, 5*1/(self.radius))
        plt.setp(self.circle, radius=self.radius, alpha=self.alpha, center=self.pos)
        #plt.getp(self.circle)

    def as_circle(self):
        return self.circle


fig = plt.figure()
ax = fig.add_axes([0,0,1,1], frameon=False)
ax.set_xlim(-200,200)
ax.set_ylim(-200,200)
ax.axis('equal')

# d = Raindrop(1,1)
drops = [ Raindrop(rand_pos(-200,200)) for i in range(50)]

total_frames = 250
pbar = tqdm(total=total_frames)

def animate(t):
    cur_idx = t % len(drops)
    d = drops[cur_idx]
    d.restart = True
    for d in drops:
        d.tick()
    pbar.update(1)
    

def init():
    for d in drops:
        ax.add_patch(d.as_circle())


ani = animation.FuncAnimation(fig, animate,total_frames, init_func=init, interval=20)

ani.save('raindrops.mp4', writer = 'ffmpeg')