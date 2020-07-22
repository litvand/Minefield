from physutil import *
from geom     import *
from vec      import *
from util     import del_unordered
from sap      import CircleSAP

class Mines:

    def update_vel_toward_tgt(self, mine_index):
        dir = unit_vec(self.poss[mine_index], self.tgts[mine_index])
        self.vels[mine_index] = vec_scale(dir, self.max_speed)

    def set_tgt(self, mine_index, tgt):
        self.tgts[mine_index] = tgt
        self.update_vel_toward_tgt(mine_index)

    def is_tgt(self, mine_index):
        return self.tgts[mine_index] is not None

    def get_tgt_dist(self, mine_index):

        if not self.is_tgt(mine_index):
            return None

        tgt  = self.tgts[mine_index]
        pos  = self.poss[mine_index]
        dist = vec_dist(pos, tgt)
        return max(0.0, dist - self.rad)

    def get_new_tgt(self, mine_index, ball_poss, wall):
        # Return the closest ball's position that is visible and
        # is closer than the current target, if there is one.

        mine_pos = self.poss[mine_index]

        visible_ball_poss = ball_poss
        is_mine_on_wall = False # TODO
        if not self.is_magnetic and not is_mine_on_wall:
            # TODO: Check circle, not point visibilty (pass ball_rad).
            visible_ball_poss = get_visible_poss(mine_pos, ball_poss, wall)

        nearest_visible, sqr_dist_nearest = get_nearest(mine_pos, visible_ball_poss)
        if nearest_visible is None: # No visible balls
            return None

        nearest_visible_pos = ball_poss[nearest_visible]
        return nearest_visible_pos

    def update_tgts(self, ball_poss, wall):
        for i in range(len(self.vels)):
            new_tgt = self.get_new_tgt(i, ball_poss, wall)
            if new_tgt is None: # There are no visible balls close enough.
                dist = self.get_tgt_dist(i)
                is_at_tgt = (dist == 0.0)
                if is_at_tgt:
                    self.tgts[i] = None
            else:
                self.set_tgt(i, new_tgt)

    def move(self, wall, dt):
        move_circles(self.poss, self.vels, self.rad, wall, dt)

    def update_collided(self):
        self.sap.find_collisions(self.poss, self.has_collided, self.rad)

    def del_collided(self):
        per_mine_lists = (self.poss, self.vels, self.tgts, self.has_collided)
        collided_num = 0
        for i in range(len(self.vels) - 1, -1, -1):
            if self.has_collided[i]:
                del_unordered(per_mine_lists, i)
                collided_num += 1
        self.del_num += collided_num
        # return collided_num   ?

# Public:

    def reset(self):
        self.poss = []
        self.vels = []
        self.tgts = []
        self.has_collided = []
        self.del_num = 0
        self.sap = CircleSAP()
        self.max_num = 0 # For debugging

    def __init__(self, world):
        self.is_magnetic = world.are_mines_magnetic
        self.max_speed   = world.mine_max_speed
        self.rad         = world.mine_rad
        self.reset()

    def get_del_num(self):
        return self.del_num

    def get_poss(self):
        return self.poss

    def get_collisions_statuses(self): # List of bools with length `mine_num`
        return self.has_collided

    def find_ball_collisions(self, ball_poss, ball_rad): # TODO: Optimize this.
        are_ball_collisions = [False] * len(ball_poss)
        max_collision_dist = ball_rad + self.rad
        max_collision_sqr_dist = max_collision_dist * max_collision_dist
        for i in range(len(ball_poss)):
            for j in range(len(self.vels)):
                sqr_dist = vec_sqr_dist(ball_poss[i], self.poss[j])
                is_collision = (sqr_dist <= max_collision_sqr_dist)
                are_ball_collisions[i] = are_ball_collisions[i] or is_collision
                self.has_collided[j]   = self.has_collided[j]   or is_collision
        return are_ball_collisions

    def explode(self):
        for i in range(len(self.vels)):
            self.has_collided[i] = True

    def advance(self, ball_poss, wall, dt):
        self.del_collided()
        # Delete already collided mines *before* checking for new ones, so
        # collided mines exist between two frames after `advance`
        # returns and the drawer/AI can get them.
        self.update_tgts(ball_poss, wall)
        self.move(wall, dt)
        self.update_collided()

    def add(self, pos):
        
        self.poss.append(pos)
        self.vels.append((0.0, 0.0))
        self.tgts.append(None)
        self.has_collided.append(False)
        
        n = len(self.poss)
        if n > self.max_num:
            self.max_num = n
            #print('Mine num:\t' + str(n))
