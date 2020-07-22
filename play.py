import random
from mineinput import *
from ballinput import *
from world     import World
from window    import Window
from sim       import Simulator

# TODO: Test each mine input and ball input, mine bitmap printing and drawing,
#       mask / other optional drawing and various combinations of keypresses,
#       mouse clicks and scrolling.

class InputCycle:
# Takes two or more input classes, all with the same parent, and
# allows the player to cycle between them by pressing a key,
# changing which input will be used to simulate frames.

    # Variables: inputs, cur, cycle_key

# Public:

    def __init__(self):
        pass

def get_simple_world():

    # TODO: Eliminate the need for this sort of comment:

    #initial_wall_bitmap,
    #mine_max_speed, mine_rad, are_mines_magnetic,
    #ball_max_speed, ball_rad, initial_ball_poss,
    #width_in_tiles, height_in_tiles, tile_width, tile_height,
    #power_fill_speed, full_power_level, explosive_power_level,
    #min_spawn_time, max_spawn_time, min_ball_added_mine_dist

    return World([0],
                 70.0, 5.0, False,
                 130.0, 5.0, ((150.0, 150.0),),
                 1, 1, 600.0, 600.0,
                 100.0, 100.0, None,
                 0.15, 0.25, 100.0)

def get_mine_input(world, window):
    # return RandomMineInput()
    # return ClassicMineAI()
    return UniformMineInput()
    # return MinePlayer(window, 0.2)

    # spawn_poss = ((50.0, 50.0), (50.0, 550.0), (550.0, 550.0), (550.0, 50.0))
    spawn_poss = []
    n = 5
    for i in range(n):
        y = world.height / float(n) * float(i)
        dx = 10.0
        spawn_poss.append((0.0 + dx, y))
        spawn_poss.append((world.width - dx, y))
    return FixedMineInput(spawn_poss)

def play():
    print('Move ball with WASD. Add mines with scroll wheel.')
    print('Press P to pause/unpause or ESC to exit.')

    random.seed(314159)

    world = get_simple_world()
    window = Window(int(world.width), int(world.height))
    mine_input = get_mine_input(world, window)
    ball_input = BallPlayer(window)
    sim = Simulator(world, window, True, False, 60, 1.0/200.0, 1.0/4.0)
    sim.run(mine_input, (ball_input,))
