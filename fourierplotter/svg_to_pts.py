import cmath
import matplotlib.pyplot as plt
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close, Move
from svg.path import parse_path
import numpy as np
from xml.dom import minidom

class SVG_Reader():
    def __init__(self, filename):
        self.config = {
            'total_pts': 2000,
            'filename': filename
        }
        self.read_file()

    def read_file(self,):
        filename = self.config['filename']
        doc = minidom.parse(filename)  # parseString also exists
        path_strings = [parse_path(path.getAttribute('d')) for path
                        in doc.getElementsByTagName('path')]
        doc.unlink()
        self.paths = path_strings
        return path_strings

    def interpolate(self):
        # distribute points to each path
        total_pts = self.config['total_pts']
        total_len = sum([p.length() for p in self.paths])
        pts_distrb = [ total_pts*p.length()/total_len for p in self.paths]

        pts = []
        cur_pt_idx, target_pt_idx = 0, 0
        step = 1 / total_pts
        for p_idx, p in enumerate(self.paths):
            target_pt_idx = cur_pt_idx + pts_distrb[p_idx]
            while cur_pt_idx < target_pt_idx:
                input_x = step * cur_pt_idx
                if input_x >= 1:
                    input_x = 1
                val = p.point(input_x)
                interpolated_val = complex(val.real, -val.imag)
                res = {
                    'pt_idx': cur_pt_idx,
                    'input_x':  input_x,
                    'val': interpolated_val
                }
                pts.append(res)
                cur_pt_idx += 1
        self.pts = pts
        return pts

    def show_points(self):
        x = [ p['val'].real for p in self.pts]
        y = [ p['val'].imag for p in self.pts]
        plt.scatter(x,y,marker='o', color="red")
        # for idx, pt in enumerate(self.pts):
        #     plt.annotate(pt['pt_idx'], (x[idx],y[idx]))
        plt.show()

    def get_pts(self):
        pass


def main():
    reader = SVG_Reader('./gears.svg')
    pts = reader.interpolate()
    for p in pts:
        print(p)
    reader.show_points()