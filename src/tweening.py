'''
Created on Dec 3, 2012

@author: Robert Rouhani
@copyright: Copyright (c) 2012, Robert Rouhani

@license: MIT
@version: 0.1
'''

def smoothstep(edge0, edge1, x):
    x = min(1, max(0, (x - edge0) / (edge1 - edge0)))
    return x * x * (3 - 2 * x)

def smootherstep(edge0, edge1, x):
    x = min(1, max(0, (x - edge0) / (edge1 - edge0)))
    return x * x * x * (x * (x * 6 - 15) + 10)