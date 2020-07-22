from minemap import *
from window import keys

class BallInput: # Trivial implementation
    def calc_vel(self, ps, ball_index):
        return (0.0, 0.0)

class BallPlayer:  # Player controls movement of one ball.

# Public:

    def __init__(self, window):
        self.key_up    = keys.W
        self.key_left  = keys.A
        self.key_down  = keys.S
        self.key_right = keys.D
        self.window    = window

    def calc_vel(self, ball_index, ps):
        
        perf_test = get_mine_bitmap(ball_index, ps)
        
        window = self.window
        up    = 1 if window.is_pressed(self.key_up)    else 0
        left  = 1 if window.is_pressed(self.key_left)  else 0
        down  = 1 if window.is_pressed(self.key_down)  else 0
        right = 1 if window.is_pressed(self.key_right) else 0

        dx = float(right - left)
        dy = float(up    - down)

        s = ps.get_balls().max_speed
        if dx != 0.0 and dy != 0.0:
            inv_sqrt_2 = 0.70710678118
            s *= inv_sqrt_2

        return (dx * s, dy * s)

class ClassicBallAI:
    def __init__(self):
        pass

    def calc_vel(self, ball_index, ps):
    
        is_mine = get_mine_bitmap(ball_index, ps)
        
        # Find shortest path to bitmap edge using Djikstra (or best-first search?).
        # Use circle-AABB collision tests to determine available adjacent nodes.
        # Increase ball rad with time (cur path len) to simulate mine movement.
        # Return vel toward first node of shortest path.
        
        return (0.0, 0.0)

class NeuralNetBallAI:
    def __init__(self):
        pass
