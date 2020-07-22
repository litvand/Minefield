from wall     import Wall
from spawner  import Spawner
from balls    import Balls
from mines    import Mines
from mathutil import *
from geom     import *
#import clouds ?

class PhysicsState:

    instance_num = 0

    def update_ball_vels(self, ball_inputs):
        vels = []
        ids = self.balls.get_ids()
        for ball_index in range(len(ids)):
            input_index = ids[ball_index]
            input = ball_inputs[input_index]
            # The AI needs to know everything that could possibly
            # affect the ball - that is, the whole const PhysicsState -
            # so pass `self`.
            # Also give a ball index to the input so the AI knows
            # which ball it's controlling.
            vel = input.calc_vel(ball_index, self)
            vels.append(vel)
        self.invalidate_public_data()
        self.balls.set_vels(vels)

    def get_nearest_ball_sqr_dist(self, pos):
        # TODO: `sqr_dist` should be shortest path distance.
        nearest_ball_pos, sqr_dist = get_nearest(pos, self.balls.get_poss())
        return sqr_dist

    def can_add_mine(self, pos):
        is_collision = (self.wall.is_circle_collision(pos, self.mines.rad))
        sqr_dist = self.get_nearest_ball_sqr_dist(pos)
        return self.spawner.can_add_mine(sqr_dist) and not is_collision

    def maybe_add_mine(self, mine_input):

        pos = mine_input.calc_pos(self) # const self
        self.invalidate_public_data()
        if not pos:
            return

        sqr_dist = self.get_nearest_ball_sqr_dist(pos)
        if not self.spawner.try_add_mine(pos, sqr_dist):
            # TODO: Notify of failure to spawn mine at `pos`.
            pass

    def maybe_spawn_mine(self):
        pos = self.spawner.try_take_live_mine()
        if pos is not None:
            self.mines.add(pos)

    # For SimplePhysicsState:
    # def move_mines_without_walls(self, dt): # Mines could be moved in parallel.
    #     for i in range(0, len(self.mine_poss)):
    #         self.update_mine_vel(i, self.ball_pos)
    #         self.mine_poss[i] += vec_scale(self.mine_vels[i], dt)

# Public (including constants):

    def reset(self, initial_wall_bitmap):

        assert(self.can_mutate)

        self.elapsed_time = KahanSum()

        # TODO: switches and goals and hives
        self.wall.reset(initial_wall_bitmap)
        self.spawner.reset()
        self.balls.reset()
        self.mines.reset()

    def __init__(self, world):

        self.id = type(self).instance_num # const and public
        type(self).instance_num += 1

        # TODO: switches and goals and hives
        self.spawner = Spawner(world)
        self.wall    = Wall(world)
        self.mines   = Mines(world)
        self.balls   = Balls(world)

        self.elapsed_time = KahanSum()

        self.can_mutate = True

    # `get_*` functions return constant values (including elements of lists).

    # If public data has been retrieved by, for example, calling
    # `physics_state.get_mines`, then it must be invalidated before
    # mutating the PhysicsState (for example, by calling `advance`).
    # After invalidation, `get_mines` must be called again for new data.
    def invalidate_public_data(self):
        self.can_mutate = True

    def get_elapsed_time(self):
        return self.elapsed_time.get()

    def get_mines(self):
        self.can_mutate = False
        return self.mines

    def get_balls(self):
        self.can_mutate = False
        return self.balls

    def get_spawner(self):
        self.can_mutate = False
        return self.spawner     # Also constant - can't spawn mines.

    def get_wall(self):
        self.can_mutate = False
        return self.wall

    # TODO: switches, goals, hives

    def has_finished(self):
        arent_any_balls = (len(self.balls.get_poss()) == 0)
        are_all_goals_reached = False # TODO
        return arent_any_balls or are_all_goals_reached

    def toggle_invincible_balls(self):
        assert(self.can_mutate)
        self.balls.toggle_invincibility()

    def advance(self, mine_input, ball_inputs, dt):

        assert(self.can_mutate)

        if self.has_finished():
            return False

        # Simulate spawner.
        self.spawner.advance(dt)
        self.maybe_spawn_mine()

        # Use inputs.
        self.update_ball_vels(ball_inputs)
        self.maybe_add_mine(mine_input)    # Allow AI to prevent explosion.
        if self.spawner.is_exploding():
            self.mines.explode()

        # Simulate balls.
        self.balls.advance(self.wall, dt)

        # Simulate mines.
        ball_poss = self.balls.get_poss()
        self.mines.advance(ball_poss, self.wall, dt)

        # Simulate ball-mine collisions.
        collisions = self.mines.find_ball_collisions(ball_poss, self.balls.rad)
        self.balls.update_collided(collisions)
        if any(collisions):
            print('time:\t' + str(self.get_elapsed_time())) # For debugging

        # Finish step.
        self.elapsed_time.add(dt)
        return True
