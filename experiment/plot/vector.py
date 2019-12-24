import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Arrow

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
#patch = plt.Circle((5, -5), 0.75, fc='y')
patch = Circle((5, -5), 0.75, fc='y')
arr = Arrow(0,0,1,1)


class vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_patch()
        this.patch = Arrow()
        
    
    def get_patch():


def init():
    patch.center = (5, 5)
    ax.add_patch(patch)
    ax.add_patch(arr)
    return patch,arr

def animate(i):
    x, y = patch.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    patch.center = (x, y)
    arr.width = arr.width + 1
    return patch,arr

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=360, 
                               interval=20,
                               blit=True)

plt.show()