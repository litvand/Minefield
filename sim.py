import time
from mathutil import *
from ps       import PhysicsState
from window   import *
from drawer   import Drawer
from minemap  import *

class Simulator:

    def run_physics(self, mine_input, ball_inputs): # Ignores `is_paused`.
        while ((self.window is None or not self.window.is_pressed(keys.ESCAPE)) and
               self.ps.advance(mine_input, ball_inputs, self.fixed_dt)):
            pass

    def handle_input(self): # Pause (menu), exit, etc when appropriate keys are pressed.

        cur_time = time.monotonic()
        if (self.last_toggle_time is None or (cur_time - self.last_toggle_time > 0.5)):

            old = self.last_toggle_time
            self.last_toggle_time = cur_time # Might be changed back.
            
            if self.window.is_pressed(keys.P):
                self.is_paused = not self.is_paused
            elif self.window.is_pressed(keys.I):
                self.ps.toggle_invincible_balls()
            elif self.window.is_pressed(keys.M):
                print_mine_bitmap_around_ball(0, self.ps)
                self.ps.invalidate_public_data()
            else:
                self.last_toggle_time = old # Avoid duplicate assignments in `elif`s.
                
        keep_going = not self.window.is_pressed(keys.ESCAPE)
        return keep_going

    def stop(self):
        self.window.on_update(None)
        # self.window.on_draw(None)

    def update(self, mine_input, ball_inputs, dt):
        # http://gafferongames.com/game-physics/fix-your-timestep/

        if self.ps.has_finished() or not self.handle_input():
            self.stop()
        if self.is_paused:
            return

        dt = min(dt, self.max_dt) # Limit frame length.
        self.unused_dt.add(dt)
        while self.unused_dt.get() >= self.fixed_dt:
            self.ps.advance(mine_input, ball_inputs, self.fixed_dt)
            self.unused_dt.add(-self.fixed_dt)

        # Drawer should be finished using `ps_to_draw` at this point.

        # TODO: copy `self.ps`.
        # self.ps_to_draw.copy(self.ps)
        # if self.unused_dt.get() >= self.dt_eps:
              # Extrapolate instead of interpolating.
        #     self.ps_to_draw.advance(self.unused_dt.get())

        # Drawer may use `ps_to_draw` again.
        return

    def draw(self):
        self.drawer.draw(self.ps_to_draw, self.is_paused)
        self.ps_to_draw.invalidate_public_data()

    def run_and_draw(self, mine_input, ball_inputs):

        self.unused_dt = KahanSum()

        # TODO: self.ps_to_draw = PhysicsState()
        self.ps_to_draw = self.ps

        update = lambda dt: self.update(mine_input, ball_inputs, dt)
        draw   = lambda:    self.draw()

        self.window.on_update(update, self.fps)
        self.window.on_draw(draw)
        self.window.run()

# Public:

    def reset(self, initial_wall_bitmap):
        self.ps.reset(initial_wall_bitmap)
        if self.drawer is not None:
            self.drawer.reset()

    def __init__(self, world, window = None, do_draw = False, use_simple_physics = False,
                 fps = 60, dt_eps = 0.005, max_dt = 0.25):

        # Constants:
        self.fps = fps
        self.fixed_dt = 1.0 / float(fps)
        self.dt_eps   = dt_eps
        self.max_dt   = max_dt
        # TODO: Copy bitmap so we can reset walls later?
        # self.initial_wall_bitmap = list(world.initial_wall_bitmap) # const copy

        # Variables:

        self.ps = PhysicsState(world)
        # TODO: if use_simple_physics: self.ps = SimplePhysicsState(...)
        self.unused_dt = None

        self.window = window
        if do_draw:
            assert(window is not None)
            self.drawer = Drawer(window)
            # if use_simple_physics:
            #   ...
            # else:
            #   self.ps_to_draw = PhysicsState(None) # Scratch memory
        else:
            self.ps_to_draw = None
            self.drawer     = None

        self.is_paused = True
        self.last_toggle_time = None

    def print_results(self):
        print('del num:\t' + str(self.ps.get_mines().get_del_num()))
        print('time:\t\t' + str(round(self.ps.get_elapsed_time(), 3)))

    def run(self, mine_input, ball_inputs):
        if self.drawer is None:
            self.run_physics(mine_input, ball_inputs)
        else:
            self.run_and_draw(mine_input, ball_inputs)
        self.print_results()

    def was_interrupted(self):
        # The player exited the level, though it wasn't completed yet
        # and at least one ball was still alive.
        return not self.ps.has_finished()

    def get_elapsed_time(self):
        return self.ps.get_elapsed_time()
