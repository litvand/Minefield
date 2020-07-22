import math
from mathutil import *
from util     import del_unordered
sqrt = math.sqrt

class Spawner:  # Used by PhysicsState.

    def get_add_cost(self, ball_sqr_dist): # Might be duplicated in pixel shader.

        if ball_sqr_dist == 0.0:
            return self.max_add_cost

        assert(ball_sqr_dist > 0.0)
        ball_dist = sqrt(ball_sqr_dist)

        linear_cost = self.full_power_level + self.min_ball_added_mine_dist - ball_dist
        return clamp(linear_cost, self.min_add_cost, self.max_add_cost)

    def get_post_add_power_level(self, ball_sqr_dist):
        cost = self.get_add_cost(ball_sqr_dist)
        p = min(self.power_level, self.full_power_level)
        return p - cost

# Public (including constants):

    def reset(self):
        self.power_level       = 0.0
        self.poss              = []
        self.times_until_spawn = []
        # self.total_spawn_times = []   ?

    def __init__(self, world):

        # Constants:
        self.power_fill_speed      = world.power_fill_speed
        self.full_power_level      = world.full_power_level
        self.explosive_power_level = world.explosive_power_level
        self.min_spawn_time        = world.min_spawn_time
        self.max_spawn_time        = world.max_spawn_time
        self.min_ball_added_mine_dist = world.min_ball_added_mine_dist
        
        self.min_add_cost = 0.1 * world.full_power_level # Not cosmetic
        self.max_add_cost = 1.1 * world.full_power_level # Cosmetic

        assert(self.min_spawn_time > 0.0)
        assert(self.min_spawn_time <= self.max_spawn_time)
        assert(self.power_fill_speed > 0.0)
        assert(self.full_power_level > 0.0)
        assert(self.explosive_power_level is None or
               self.explosive_power_level >= self.full_power_level)

        self.reset()

    # `get_*` returns constant values.

    def get_add_power_level(self):
        return min(self.power_level, self.full_power_level)

    def get_poss(self):
        return self.poss

    def get_times_until_spawn(self):
        return self.times_until_spawn

    def get_time_until_explosion(self):
        if self.explosive_power_level is None:
            return None
        d = self.explosive_power_level - self.power_level
        t = d / self.power_fill_speed
        return max(t, 0.0)

    def is_full_power_level(self):
        return self.power_level >= self.full_power_level

    def is_exploding(self):
        return self.get_time_until_explosion() == 0.0

    def can_add_mine(self, ball_sqr_dist):
        return self.get_post_add_power_level(ball_sqr_dist) >= 0.0

    def try_add_mine(self, mine_pos, ball_sqr_dist):

        if not self.can_add_mine(ball_sqr_dist):
            return False

        self.power_level = self.get_post_add_power_level(ball_sqr_dist)
        self.poss.append(mine_pos)
        time_until_spawn = get_uniform_rand(self.min_spawn_time, self.max_spawn_time)
        # TODO: Also append to `total_spawn_times` for drawer? (draw various spawn vels)
        self.times_until_spawn.append(time_until_spawn)
        return True

    def try_take_live_mine(self):
        for i in range(len(self.poss)):
            if self.times_until_spawn[i] <= 0.0:
                pos = self.poss[i]
                # Delete from each list containing per-mine data.
                del_unordered((self.poss, self.times_until_spawn), i)
                return pos
        return None

    def advance(self, dt):
        for i in range(len(self.poss)):
            self.times_until_spawn[i] -= dt
        # Given a sufficiently smart Python interpreter, the
        # next line will become a fused multiply-add instruction.
        self.power_level += self.power_fill_speed * dt
