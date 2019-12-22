import matplotlib.pyplot as plt
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close
from svg.path import parse_path
import numpy as np


def read_svg(svg_file):
    from xml.dom import minidom
    doc = minidom.parse(svg_file)  # parseString also exists
    path_strings = [parse_path(path.getAttribute('d')) for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()
    return path_strings


path1 = parse_path('M 100 100 L 300 100 L 200 300 z')
path2 = parse_path('M600,200 C675,100 975,100 900,200')
#paths = [path1, path2]
paths = read_svg("./imgs/badge.svg")


total_pts = 100
total_len = sum( p.length() for p in paths)

def subdiv_pts( total_pts, total_len, cur_len):
    return total_pts * cur_len/total_len

print(f'total: {total_len}')
total = 0
for idx, path in enumerate(paths):
    path_len = path.length()
    path_pts = subdiv_pts(total_pts,total_len,path_len)

    print(f'path: {idx}, len:{path_len}')
    if path_len == 0:
        continue
    for seg_idx, seg in enumerate(path):
        seg_len = seg.length()
        seg_pts = subdiv_pts(path_pts,path_len,seg_len)
        total += seg_len
        print(f'  seg{seg_idx}: len={seg_len:5.2f}, total:{total:5.2f}, num_pts:{seg_pts:5.2f}')

        if seg_pts == 0:
            continue
        print(f' total:{total:5.2f}')
        for i in np.arange(0, 1, 1/seg_pts):
            val = path.point(i)
            n = complex(val.real, -1*val.imag)
            print(f'        ({n.real:5.2f},{n.imag:5.2f})')
            #print(f' {num}')
            plt.plot(n.real, n.imag, marker='o', markersize=3, color="red")

# plt.show()
