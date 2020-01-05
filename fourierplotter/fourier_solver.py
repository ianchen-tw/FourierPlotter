import cmath
from dataclasses import dataclass
from typing import List
import math

@dataclass
class DiscreteComplexRelation:
    # mapping btw real value input and complex output value
    in_x: float
    val: complex

def complex_fourier_analysis( relations:List[DiscreteComplexRelation], total_pow:int):
    '''the range of power is [-total_pow,total_pow]
    '''
    ret = { 'total_terms': 2*total_pow+1}
    for n in range(-total_pow, total_pow+1):
        ret[n] = None
    total_pts = len(relations)
    for n in range(-1*total_pow,total_pow+1):
        # calculate for each term
        total = 0+0j
        for r in relations:
            total += r.val * cmath.exp(-n*2*math.pi*1j*r.in_x)
        ret[n] = total/total_pts
    return ret
