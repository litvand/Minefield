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
    return World(
        initial_wall_bitmap=[0],
        mine_max_speed=60.0, mine_rad=5.0, are_mines_magnetic=False,
        ball_max_speed=130.0, ball_rad=5.0, initial_ball_poss=((150.0, 150.0),),
        width_in_tiles=1, height_in_tiles=1, tile_width=600.0, tile_height=600.0,
        power_fill_speed=100.0, full_power_level=100.0, explosive_power_level=None,
        min_spawn_time=0.15, max_spawn_time=0.25, min_ball_added_mine_dist=50.0
    )

def get_mine_input(world, window):
    '''Select who to play against here:''' 
    return RandomMineInput()
    # return ClassicMineAI()
    # return UniformMineInput()
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
    sim = Simulator(
        world, window, do_draw=True, use_simple_physics=False,
        fps=60, dt_eps=0.005, max_dt=0.25
    )
    sim.run(mine_input, (ball_input,))

play()


