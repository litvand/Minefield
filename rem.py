class Area: # REM

# Public:

    def __init__(self, center, half_width, half_height,
                 can_mine_trigger, can_ball_trigger, world):

        # Constants:
        self.world = world # REM?
        self.can_trigger = (can_ball_trigger, can_mine_trigger)

        # Variables:

        #self.center  = center  # REM
        self.is_on = False

    def try_trigger(self, pos, is_mine): # not is_mine == is_ball

        if not self.can_trigger[is_mine]:
            return False

        rad = world.mine_rad if is_mine else World.ball_rad
        if isCircleTouchingAABB(pos, rad, self.corner_a, self.corner_b):
            self.trigger()
            return True
        return False

    def notify_wall_change(self, walls):
        pass

def should_be_on(switch_wall_tiles, is_wall, is_del_switch): # REM?
    for i in range(len(switch_wall_tiles)):
        if is_wall[map.width_in_tiles * y + x] == is_del_switch:
            return True
    return False

class Switch:  # Triggers destruction or creation of walls.
    pass

class Goal:    # What the ball needs to reach
    pass

class Hive:    # Where mines spawn
    pass

# TODO: `class SimplePhysicsState` using TensorFlow (ignores walls and switches)

class Menu: # Not even sure where this will go anymore...

# Public:

    def __init__(self):
        pass
