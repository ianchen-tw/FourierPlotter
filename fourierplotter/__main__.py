import click
import pathlib
import errno
import os

from .svg_to_pts import SVG_Reader
from .plotter import Plotter
from .fourier_solver import DiscreteComplexRelation, complex_fourier_analysis

@click.command()
@click.argument( 'input_file')
@click.option('--output', default='fourier_plotter.mp4', show_default=True)
@click.option('--dpi', type=int, default=100, help="dpi for output image")
@click.option('--verbose', type=bool, default=True, help='show progress bar')
@click.option('--preview', is_flag=True, default=False, help='compute and preview outcome in real time')
@click.option('--num_terms', type=int, default=500, help="number of terms to approximate your image", show_default=True)
@click.option('--duration', type=float, default=10, help="video length (in second)", show_default=True)
def fourier_plotter(dpi, output, input_file, verbose, preview, num_terms, duration):
    if verbose:
        print(f'dpi = {dpi}')
        print(f'output = {output}')
        print(f'input = {input_file}')
        print(f'verbose = {verbose}')
        print(f'preview = {preview}')
        print(f'num_terms = {num_terms}')
        print(f'duration = {duration:.2f} sec')

    # read in svg file
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

    num_terms = num_terms//2
    num_terms = num_terms if num_terms >=1 else 1
    # dictionary of solved terms
    ret = complex_fourier_analysis(pts_in, num_terms)

    # plot data to file
    plotter = Plotter(verbose=True)
    total_frames = int(duration*1000/plotter.config['draw_interval'] )
    plotter.set_config( output_filename=output, total_frames=total_frames, dpi=dpi)
    plotter.read_data(ret)
    plotter.draw(live=preview)

if __name__ == "__main__":
    fourier_plotter()