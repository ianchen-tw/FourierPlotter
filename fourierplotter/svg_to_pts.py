import cmath
import matplotlib.pyplot as plt
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close, Move
from svg.path import parse_path
import numpy as np
from xml.dom import minidom

def to_string(seg):
    if type(seg) == Path:
        return f'Path( length:{seg.length():.2f}, #segs:{len(seg._segments)})'
    if type(seg) == Line:
        return  f'Line(start={seg.start:.2f}, end={seg.end:.2f})'
    elif type(seg) == CubicBezier:
        return f"CubicBezier(start={seg.start:.2f}, control1={seg.control1:.2f}, control2={seg.control2:.2f}, end={seg.end:.2f})"
    elif type(seg) == QuadraticBezier:
        return f"QuadraticBezier(start={seg.start:.2f}, control={seg.control:.2f}, end={seg.end:.2f})"
    elif type(seg) == Arc:
        return f"Arc(start={seg.start:.2f}, radius={seg.radius:.2f}, rotation={seg.rotation:.2f}, arc={seg.arc:.2f}, sweep={seg.sweep:.2f}, end={seg.end:.2f})"
    return f'unknown seg type:{type(seg)}, detail:{seg}'

class SVG_Reader():
    def __init__(self, filename):
        self.config = {
            # TODO: export total_pts as an option
            'total_pts': 5000,
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
        cur_pt_idx = 0
        step = 1 / total_pts
        for p_idx, p in enumerate(self.paths):
            # show path information
            # print(f'{to_string(p)}')

            cur_path_pts = pts_distrb[p_idx]
            step = abs(1 / cur_path_pts)
            input_x = 0
            cur_pt_idx =0
            while True:
                input_x = step * cur_pt_idx
                if input_x > 1:
                    break
                val = p.point(input_x)
                interpolated_val = complex(val.real, -val.imag)
                res = {
                    'pt_idx': cur_pt_idx,
                    'input_x':  input_x,
                    'val': interpolated_val
                }
                pts.append(res)
                cur_pt_idx += 1

        # normalize
        minx = min( [ p['val'].real for p in pts])
        maxx = max( [ p['val'].real for p in pts])
        miny = min( [ p['val'].imag for p in pts])
        maxy = max( [ p['val'].imag for p in pts])
        # print(f'min:({minx},{miny}), max:({maxx},{maxy})')

        scale_x = 1.0/(maxx-minx)
        shift_x = -minx
        scale_y = 1.0/(maxy-miny)
        shift_y = -miny
        for p in pts:
            new_x = scale_x*(shift_x+p['val'].real)
            new_y = scale_y*(shift_y+p['val'].imag)
            p['val'] = complex( new_x, new_y)
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

if __name__ == "__main__":
    reader = SVG_Reader('./sample_input/shirt.svg')
    pts = reader.interpolate()
    for p in pts[:100]:
        print(p)
    print(f'len :{len(pts)}')