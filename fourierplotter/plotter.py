import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Arrow
from math import sin, cos
import math
from random import randint, random, choice
from typing import Dict
import cmath
import sys
from tqdm import tqdm

def compute_term(n, coffi, i):
    ''' n : The Nth frequency term
        coffi: coffieicnet for your term
        i : the angle for your circle
    '''
    return coffi * cmath.exp(n*2*math.pi*1j*i)


def point_idx_to_term(idx):
    '''
        Convert point indices to the terms it represent.

        idx| 0 |  1 | 2 |  3 | 4 |
        --------------------------
           | 0 | -1 | 1 | -2 | 2 |
    '''
    if idx == 0:
        return 0
    residual = (idx-1) % 2
    term_abs = (idx+1) // 2
    term = term_abs * -1 if residual == 0 else term_abs
    return term


# TODO:
#   specify the time of the output video, not just number of frames
class Plotter:
    def __init__(self, verbose=True):
        self.config = {
            'verbose': verbose,
            'input_data': None,
            'output_filename': 'fourier_plot.mp4',
            'input_filename': 'something.svg',
            'total_frames': 1000
        }

        # if self.config['verbose']==True:
        #     self.pbar = tqdm(total=self.config['total_frames'])

        # self.read_data()
        # figure
        self.plt = plt
        self.fig = plt.figure()
        self.fig.set_dpi(100)
        self.fig.set_size_inches(7, 6.5)


        # gears
        # self.ax = plt.axes(xlim=(1500000, 3000000),  ylim=(-3500000,0))

        # download
        # self.ax = plt.axes(xlim=(500000, 2500000),  ylim=(-3000000,0))

        # shirt
        # self.ax = plt.axes(xlim=(0, 2500000),  ylim=(-3000000,1000000))

        # office
        self.ax = plt.axes(xlim=(0, 300000),  ylim=(-300000,0))

        # raw data serve as a numpy source datatsture for plot_data to use
        self.raw_data = None

        line, = self.ax.plot([], [], 'o-', lw=3)
        trace_line, = self.ax.plot([], [], 'o-', lw=3)
        self.plot_data = {
            'line': line,
            'trace_line': trace_line,
        }

    def set_config(self,  **kwargs ):
        configable_options = set([
            'verbose','output_filename','total_frames'
            ])
        for k,v in kwargs.items():
            if k in configable_options:
                # print(f'config k={k}, v={v}')
                self.config[k] = v

    def read_data(self, d:Dict):
        self.config['input_data'] = d
        self.raw_data = {
            'line_pts': np.zeros(
                self.config['input_data']['total_terms'], dtype=[('x', float, (1,)), ('y', float, (1,)), ]),
            'trace_line_pts': np.zeros(self.config['total_frames'], dtype=[
                ('x', float, (1,)), ('y', float, (1,)), ])
        }
        return True

    def animate_init(self):
        if self.config['verbose']:
            self.pbar = tqdm(total=self.config['total_frames'])
        self.plot_data['line'].set_data([], [])
        self.plot_data['trace_line'].set_data([], [])
        return self.plot_data.values()

    def animate(self, frame):
        rad = frame / self.config['total_frames']
        # rad = frame*0.002
        # self.raw_data

        for i in range(len(self.raw_data['line_pts'])):
            # a complex number
            term = point_idx_to_term(i)
            coffi = self.config['input_data'][term]
            if i == 0:
                x, y = 0, 0
            else:
                x, y = self.raw_data['line_pts'][i-1]
            # print(f'x:{x}, y:{y}')

            next_pos = complex(x, y) + coffi * \
                cmath.exp(term * 2 * math.pi * 1j * rad)
            self.raw_data['line_pts'][i] = next_pos.real, next_pos.imag

        # the index of data store the edge point
        edge_point_idx = len(self.raw_data['line_pts'])-1

        # print(f'frame={frame}, idx={edge_point_idx}')
        self.raw_data['trace_line_pts'][frame] = self.raw_data['line_pts'][edge_point_idx]
        # print(f"edge :{self.raw_data['line_pts'][idx]}")
        self.plot_data['line'].set_data(self.raw_data['line_pts']['x'], self.raw_data['line_pts']['y'])
        self.plot_data['trace_line'].set_data(self.raw_data['trace_line_pts']['x'][:frame], self.raw_data['trace_line_pts']['y'][:frame])

        if self.config['verbose']:
            self.pbar.update(1)

        # TODO: correct the output
        return self.plot_data['trace_line'], self.plot_data['line']

    def draw(self, live=False):
        self.animation = animation.FuncAnimation(self.fig, self.animate,
                                            init_func=self.animate_init,
                                            frames=self.config['total_frames'],
                                            interval=20,
                                            blit=True)
        # self.live_show()
        if live:
            self.live_show()
        else:
            self.save()

    def live_show(self):
        # TODO:remove progess bar once the data have be produced
        self.plt.show()

    def save(self):
        self.animation.save(self.config['output_filename'],writer='ffmpeg')


def main():
    plotter = Plotter(verbose=True)
    plotter.read_data({
            'total_terms': 5,
            -2: 8-23j,
            -1: 8+9j,
            0: 24.346+56j,
            1: 4.23-27j,
            2: 23,
    })
    plotter.draw()
    # plotter.live_show()
    #plotter.save()


if __name__ == "__main__":
    main()
