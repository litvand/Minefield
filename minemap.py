import math
from vec    import *
from geom   import *
from bitmap import Bitmap
from util   import set_str_char

def bitmap_corner_from_center(center, size_in_bits, step):
    return vec_add(center, vec_scale(size_in_bits, -0.5 * step))

# TODO: Optimize this.
def get_bitmap_of_circles_on_AABB(size_in_bits, center, step, poss, rad):

    corner = bitmap_corner_from_center(center, size_in_bits, step)
    bitmap = Bitmap(None, size_in_bits, corner, step)
    is_circle = bitmap.bits

    rad_in_bits = math.ceil(rad * bitmap.inv_step)

    for circle_index in range(len(poss)):
        circle_center = poss[circle_index]
        bit_center = bitmap.indices_from_pos(circle_center)

        for dx in range(-rad_in_bits, rad_in_bits + 1):
            for dy in range(-rad_in_bits, rad_in_bits + 1):

                bit_pos = vec_add(bit_center, (dx, dy))
                if not bitmap.are_indices_in_bounds(bit_pos):
                    # `bit_pos` isn't in bitmap, so ignore this mine.
                    # In other words, this mine isn't visible on the bitmap.
                    continue

                corner_a, corner_b = bitmap.get_bit_corners(bit_pos)
                is_touching = is_circle_touching_AABB(bit_center, rad_in_bits,
                                                      corner_a, corner_b)
                bit_index = bitmap.index_from_indices(bit_pos)
                is_circle[bit_index] = (is_circle[bit_index] or is_touching)
    return bitmap

def get_mine_bitmap(ball_index, ps):
    mines = ps.get_mines()
    rad = mines.rad
    mine_poss  = mines.get_poss()

    ball_poss  = ps.get_balls().get_poss()
    ball_pos   = ball_poss[ball_index]

    mine_bitmap_side_len = 80
    size_in_bits = (mine_bitmap_side_len, mine_bitmap_side_len)
    return get_bitmap_of_circles_on_AABB(size_in_bits, ball_pos, rad, mine_poss, rad)
        
def print_mine_bitmap_around_ball(ball_index, ps):
    mine_bitmap   = get_mine_bitmap(ball_index, ps)
    width_in_bits = mine_bitmap.size_in_bits[0]
    mein_str      = mine_bitmap.to_str('.', 'm')
    ball_index    = int((len(mein_str) - width_in_bits) / 2)
    print(set_str_char(mein_str, ball_index, 'b'))
    print('\n---\n')
