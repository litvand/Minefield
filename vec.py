import math
from mathutil import inv_sqrt
sqrt = math.sqrt

def vec_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def vec_sub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def vec_scale(a, x):
    return (a[0] * x, a[1] * x)

def vec_dot(a, b):
    return (a[0] * b[0]) + (a[1] * b[1])

def vec_sqr_len(a):
    return vec_dot(a, a)

def vec_sqr_dist(a, b):
    return vec_sqr_len(vec_sub(a, b))

def vec_len(a):
    return sqrt(vec_sqr_len(a))

def vec_dist(a, b):
    return vec_len(vec_sub(a, b))

def vec_cross_z(a, b):
    return (a[0] * b[1]) - (a[1] * b[0])

def unit_vec(a, b):
    d = vec_sub(b, a)
    return vec_scale(d, inv_sqrt(vec_sqr_len(d)))
