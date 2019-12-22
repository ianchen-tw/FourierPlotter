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

import matplotlib.pyplot as plt

for seg in paths:
  print(f'seg: {seg}')
  if seg.length() == 0:
    continue
  for i in np.arange(0,1,0.005):
    val = seg.point(i)
    n = complex(val.real, -1*val.imag)
    #print(f' {num}')
    plt.plot(n.real, n.imag,marker='o', markersize=3, color="red")

plt.show()


#print(path1)