import time
from mathutil import *
from vec      import *

class MineInput: # Trivial implementation
    def calc_pos(window, ps):
        return None # In C++, use two references (`input_pos` and `is_input`).

# This function can fail to return a suitable
# position if it runs out of time (max_try_num).
def get_rand_mine_input_pos(ps, is_immediately_addable, max_try_num):

    wall = ps.get_wall()
    width  = wall.width
    height = wall.height
    rad = ps.get_mines().rad

    try_num = 0

    while True:
        x = get_uniform_rand(0.0, width)
        y = get_uniform_rand(0.0, height)
        pos = (x, y)

        do_ret = None
        if try_num == max_try_num:
            do_ret = True
        elif is_immediately_addable:
            do_ret = ps.can_add_mine(pos)
        else:
            do_ret = (not wall.is_circle_collision(pos, rad))
        assert((do_ret == True) or (do_ret == False))

        if do_ret:
            return pos
        try_num += 1

def is_big_enough_time_diff_between_mine_adds(prev_time, ps):

    if prev_time is None:
        return True

    mines = ps.get_mines()
    eps = 0.1
    min_dist = (2.0 + eps) * mines.rad
    min_diff = min_dist / mines.max_speed

    cur_diff = ps.get_elapsed_time() - prev_time
    return cur_diff >= min_diff

class MinePlayer:  # Player controls all mines.

    def is_big_enough_time_diff(self):

        prev = self.prev_add_time
        if prev is None:
            return True

        cur  = self.time_func()
        diff = cur - prev
        return diff >= self.min_time_between_adds

    def maybe_update(self, x, y):

        if not self.is_big_enough_time_diff():
            return

        self.to_add = (x, y)
        self.prev_add_time = self.time_func()

    def on_scroll(self, cursor_x, cursor_y, scroll_x, scroll_y):
        self.maybe_update(cursor_x, cursor_y)

    def on_click(self, cursor_x, cursor_y, button, modifiers):
        self.maybe_update(cursor_x, cursor_y)

# Public:

    def __init__(self, window, min_time_between_adds = 0.0):

        self.time_func = None
        if time.get_clock_info('perf_counter').monotonic:
            self.time_func = time.perf_counter
        else:
            self.time_func = time.monotonic
            info = time.get_clock_info('monotonic')
            assert(info.monotonic)
            if info.resolution > min_time_between_adds:
                print('Warning: Best monotonic clock resolution found is ' +
                      str(resolution) + ' seconds.')
                # TODO: Adjust `min_time_between_adds`?
        assert(self.time_func is not None)

        self.min_time_between_adds = min_time_between_adds # const number of seconds
        self.to_add = None
        self.prev_add_time = None
        window.on_scroll(lambda x, y, dx, dy: self.on_scroll(x, y, dx, dy))
        window.on_click( lambda x, y, dx, dy: self.on_click(x, y, dx, dy))

    def calc_pos(self, ps):
        old = self.to_add
        self.to_add = None
        return old

def clamp_in_wall(pos, ps):
    wall = ps.get_wall()
    x = clamp(pos[0], 0.0, wall.width)
    y = clamp(pos[1], 0.0, wall.height)
    return (x, y)

class ClassicMineAI:

    def add_pos_from_dir(self, dir, dist, ps):
        offset = vec_scale(dir, dist)
        poss = ps.get_balls().get_poss()
        raw  = vec_add(poss[0], offset)
        clamped = clamp_in_wall(raw, ps)
        return clamped

# Public:

    def __init__(self):
        self.prev_time = None
        self.last_dir  = None

    def calc_pos(self, ps):
        
        if not is_big_enough_time_diff_between_mine_adds(self.prev_time, ps):
            return None
        self.prev_time = ps.get_elapsed_time()

        ball_vels = ps.get_balls().get_vels()
        if len(ball_vels) == 0:
            wall = ps.get_wall()
            return vec_scale((wall.width, wall.height), 0.5)

        vel = ball_vels[0]
        sqr_speed = vec_sqr_len(vel)
        if sqr_speed == 0.0:
            return get_rand_mine_input_pos(ps, True, 20)

        cur_dir = vec_scale(vel, inv_sqrt(sqr_speed))
        dir = cur_dir
        if self.last_dir is not None:
            sum = vec_add(cur_dir, self.last_dir)
            dir = vec_scale(sum, 0.5)
            

        self.last_dir = cur_dir
        
        pos = self.add_pos_from_dir(dir, 150.0, ps)
        if ps.can_add_mine(pos):
            return pos
        opposite_dir = vec_scale(dir, -1.0)
        return self.add_pos_from_dir(opposite_dir, 110.0, ps)

class NeuralNetMineAI:
    def __init__():
        pass

class UniformMineInput:

    def __init__(self):
        self.max_try_num = 20

    def calc_pos(self, ps):
        if ps.get_spawner().is_full_power_level():
            return get_rand_mine_input_pos(ps, True, self.max_try_num)
        return None

class RandomMineInput:

# Public:

    def __init__(self):
        self.input_pos = None
        self.max_try_num = 20

    def calc_pos(self, ps):

        # Commit to `input_pos` to ensure more uniform and FPS-independent
        # positions. Otherwise more FPS will cause mines to be spawned
        # farther from balls, because the spawner's power level will never
        # become full if mines are added frequently enough.
        if self.input_pos is None:
            self.input_pos = get_rand_mine_input_pos(ps, False, self.max_try_num)

        if ps.can_add_mine(self.input_pos):
            old = self.input_pos
            self.input_pos = None
            return old

        if ps.get_spawner().is_full_power_level(): # Add now or never.
            old = self.input_pos
            self.input_pos = None
            if ps.can_add_mine(old):
                return old
            return get_rand_mine_input_pos(ps, True, self.max_try_num)

        return None

class FixedMineInput:

    def inc(self, index):
        return (index + 1) % len(self.poss)

    def try_find_pos(self, ps):
        i = self.start
        while True:
            pos = self.poss[i]
            is_time = is_big_enough_time_diff_between_mine_adds(self.prev_times[i], ps)
            if is_time and ps.can_add_mine(pos):
                self.prev_times[i] = ps.get_elapsed_time()
                return pos

            i = self.inc(i)
            if i == self.start: # Checked all positions.
                return None

# Public:

    def __init__(self, poss):
        self.poss = tuple(poss)
        assert(len(poss) > 0)
        self.start = 0
        self.prev_times = [None] * len(poss)

    def calc_pos(self, ps):
        pos = self.try_find_pos(ps)
        if pos is not None:
            self.start = self.inc(self.start)
        return pos