from mathutil import *
from vec      import *

def is_point_in_AABB(point, corner_a, corner_b):
    #return (is_within(point[0], corner_a[0], corner_b[0]) and
    #        is_within(point[1], corner_a[1], corner_b[1]))
    return (corner_a[0] <= point[0] and point[0] <= corner_b[0] and
            corner_a[1] <= point[1] and point[1] <= corner_b[1])

# Warning: manual inling incoming

def is_circle_touching_AABB(pos, rad, corner_a, corner_b):
    
    if (corner_a[0] <= pos[0] and pos[0] <= corner_b[0] and
        corner_a[1] <= pos[1] and pos[1] <= corner_b[1]):
        return True

    closestx = min(max(pos[0], corner_a[0]), corner_b[0])
    closesty = min(max(pos[1], corner_a[1]), corner_b[1])
    dx = pos[0] - closestx
    dy = pos[1] - closesty
    sqr_dist = (dx * dx) + (dy * dy)
    return sqr_dist < rad * rad

def get_AABB_corners(center, half_width, half_height):
    assert(half_width  > 0)
    assert(half_height > 0)
    d = (half_width, half_height)
    a = vec_sub(center, d)
    b = vec_add(center, d)
    return a, b # For all i, a[i] <= b[i].

def get_nearest(a_pos, b_poss): # const params

    if len(b_poss) == 0:
        return None, None

    nearest = 0
    min_sqr_dist = vec_sqr_dist(a_pos, b_poss[nearest])
    for i in range(1, len(b_poss)):
        sqr_dist = vec_sqr_dist(a_pos, b_poss[i])
        if sqr_dist < min_sqr_dist:
            min_sqr_dist = sqr_dist
            nearest = i
    return nearest, min_sqr_dist
