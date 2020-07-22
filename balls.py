from physutil import *
from vec      import *
from util     import del_unordered

class Balls:

    def is_valid_vel(self, vel): # TODO: Adjust `eps`.
        x = self.max_speed
        eps = 0.1
        return vec_sqr_len(vel) / (x * x) <= (1.0 + eps)

    def move(self, wall, dt):
        move_circles(self.poss, self.vels, self.rad, wall, dt)

    def del_collided(self):
        per_ball_lists = (self.poss, self.vels, self.ids, self.has_collided)
        for i in range(len(self.vels) - 1, -1, -1):
            if self.has_collided[i]:
                del_unordered(per_ball_lists, i)

# Public:

    def reset(self):

        self.poss = list(self.initial_poss)
        initial_ball_num = len(self.poss)

        self.vels = [(0.0, 0.0)] * initial_ball_num
        self.has_collided = [False] * initial_ball_num
        self.ids = list(range(initial_ball_num))
        self.are_invincible_ = False

    def __init__(self, world):
        self.max_speed    = world.ball_max_speed # const and public
        self.rad          = world.ball_rad       # const and public
        self.initial_poss = list(world.initial_ball_poss) # const
        self.reset()

    def get_collision_statuses(self):
        return self.has_collided

    def get_poss(self):
        return self.poss

    def get_vels(self):
        return self.vels

    # IDs are initially (0 .. ball_num - 1). Balls may be
    # deleted, but the IDs of remaining balls stay the same.
    def get_ids(self):
        return self.ids

    def toggle_invincibility(self):
        self.are_invincible_ = not self.are_invincible_

    def are_invincible(self):
        return self.are_invincible_

    def update_collided(self, are_new_collisions):
        if self.are_invincible_:
            return # Ha!
        for i in range(len(self.poss)):
            self.has_collided[i] = self.has_collided[i] or are_new_collisions[i]
            
    def set_vels(self, vels):
        for i in range(len(vels)):
            assert(self.is_valid_vel(vels[i]))
            self.vels[i] = vels[i]

    def advance(self, wall, dt):
        self.del_collided()
        self.move(wall, dt)
