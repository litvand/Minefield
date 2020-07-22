from vec import *

# TODO: Balls or mines on top of walls see everything below them
#       and can't be seen by anyone below (no collisions).

def move_circles(poss, vels, rad, wall, dt): # const vels, wall

    assert(len(poss) == len(vels))

    # Cast `dt` to float?

    for i in range(len(poss)):
        step_without_collision = vec_scale(vels[i], dt)

        # `step` and `step_without_collision` aren't always equal
        # if there are walls that aren't the level's borders.
        step = wall.adjust_step(poss[i], rad, step_without_collision) # Handle collision.
        poss[i] = vec_add(poss[i], step)

def get_visible_poss(a_pos, b_poss, wall):
    f = lambda b_pos: wall.is_visible(a_pos, b_pos)
    return list(filter(f, b_poss))
