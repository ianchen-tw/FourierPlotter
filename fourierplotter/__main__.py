import click
import pathlib
import errno
import os

from fourierplotter.plotter import main as plt_main
from fourierplotter.svg_to_pts import main as svg_main

from .svg_to_pts import SVG_Reader
from .plotter import Plotter
from .fourier_solver import DiscreteComplexRelation, complex_fourier_analysis

@click.command()
@click.argument( 'input_file')
@click.option('--output', default='fourier_plotter.mp4', show_default=True)
@click.option('--dpi', type=int, default=100, help="dpi for output image")
@click.option('--verbose', type=bool, default=True, help='show progress bar')
@click.option('--preview', is_flag=True, default=False, help='compute and preview outcome in real time')
def fourier_plotter(dpi, output, input_file, verbose, preview):
    print(f'dpi = {dpi}')
    print(f'output = {output}')
    print(f'input = {input_file}')
    print(f'verbose = {verbose}')
    print(f'preview = {preview}')

    # read in svg file
    # input_file = 'office.svg'
    if not pathlib.Path(input_file).exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_file)
    svg_reader = SVG_Reader(input_file)

    # interpolate points
    pts = svg_reader.interpolate()
    # svg_reader.show_points()

    # apply complex fourier analysis on these discrete points
    pts_in = []
    for p in pts:
        # print(p)
        r = DiscreteComplexRelation(p['input_x'], p['val'])
        pts_in.append(r)

    # dictionary of solved terms
    ret = complex_fourier_analysis(pts_in, 1000)

    # from pprint import pprint
    # pprint(ret)

    # plot data to file
    plotter = Plotter(verbose=True)
    plotter.set_config( output_filename=output, total_frames=2000)
    plotter.read_data(ret)
    plotter.draw(live=preview)

if __name__ == "__main__":
    fourier_plotter()