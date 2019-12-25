import matplotlib.pyplot as plt
from svg.path import Path, Line, Arc, CubicBezier, QuadraticBezier, Close, Move
from svg.path import parse_path
import numpy as np

def read_svg(svg_file):
    from xml.dom import minidom
    doc = minidom.parse(svg_file)  # parseString also exists
    path_strings = [parse_path(path.getAttribute('d')) for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()
    return path_strings

# path1 = parse_path('M 100 100 L 300 100 L 200 300 z')
# path2 = parse_path('M600,200 C675,100 975,100 900,200')
#paths = [path1, path2]
paths = read_svg("./imgs/gears.svg")


total_pts = 2000

def to_string(seg):
    if type(seg) == Line:
        return  f'Line(start={seg.start:.2f}, end={seg.end:.2f})'
    elif type(seg) == CubicBezier:
        return f"CubicBezier(start={seg.start:.2f}, control1={seg.control1:.2f}, control2={seg.control2:.2f}, end={seg.end:.2f})"
    elif type(seg) == QuadraticBezier:
        return f"QuadraticBezier(start={seg.start:.2f}, control={seg.control:.2f}, end={seg.end:.2f})"
    elif type(seg) == Arc:
        return f"Arc(start={seg.start:.2f}, radius={seg.radius:.2f}, rotation={seg.rotation:.2f}, arc={seg.arc:.2f}, sweep={seg.sweep:.2f}, end={seg.end:.2f})"
    return f'unknown seg type: {seg}'

def subdiv_pts( total_pts, total_len, cur_len):
    return total_pts * cur_len/total_len

# #preprocess path:
# for path in paths:
#     cur_subpath = {}
#     for idx,seg in enumerate(path):
#         if type(seg) == Move:
#             cur_subpath['start'] = seg.start
#             cur_subpath['idx'] = idx
#         elif type(seg) == Close and cur_subpath:
#             print(f'idx:{idx}, nstart:{seg.end}, nend:{cur_subpath["start"]},pidx:{cur_subpath["idx"]} ')
#             path[idx] = Line(seg.end, cur_subpath['start'])

total_len = sum( p.length() for p in paths)
print(f'total: {total_len}')
total = 0
paths_res = []
for idx, path in enumerate(paths):
    if idx != 0:
        continue

    pts_allocated =0
    path_res = []
    path_len = path.length()
    path_pts = subdiv_pts(total_pts,total_len,path_len)

    print(f'path: {idx}, len:{path_len}')
    if path_len == 0:
        continue
    last_end = 1+1j
    for seg_idx, seg in enumerate(path):

        this_start = seg.start
        dis = this_start-last_end
        if dis.real**2 + dis.imag**2 >= 0.1:
            print(f'====================')

        seg_len = seg.length()
        seg_pts = subdiv_pts(path_pts,path_len,seg_len)

        total += seg_len
        print(f'  seg{seg_idx}, detail:{to_string(seg)}, len={seg_len:5.2f}, total:{total:5.2f}, num_pts:{seg_pts:5.2f}')
        if seg_pts == 0:
            continue
        last_end = seg.end
        for i in np.arange(0, 1, 1/seg_pts):
            val = path.point(i)
            n = complex(val.real, -1*val.imag)
            pt_res = {
                'pt':n,
                't': (pts_allocated+i) /path_pts
            }
            print(pt_res)
            path_res.append(pt_res)
            plt.plot(n.real, n.imag, marker='o', markersize=3, color="red")
        pts_allocated += seg_pts
    paths_res.append(path_res)

for pres in paths_res:
    print(f"{len(pres)}: { pres[-1]['t']}")

import cmath
total_pow = 100
for idx,pres in enumerate(paths_res):
    print(f'Path {idx}:')
    for n in range(-1*total_pow,total_pow+1):
        total = 0+0j
        for pt_res in pres:
            pt = pt_res['pt']
            t = pt_res['t']
            total += pt* cmath.exp(-1*n*2*3.14*1j*t)
        print(f'    C{n}: {total}')

plt.show()
