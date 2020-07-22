import ga
import sim

class Mimic:
# The constructor of Mimic takes two objects x and y of classes X and Y.
# X and Y must have the same parent, and the parent must be `MineInput`
# or `BallInput`. x is considered an approximation of optimal play.

# Each frame, x and y will both calculate a move. x's move will be
# used to simulate one frame. Then y is also given x's move, so y
# can estimate how far y's move was from x's move and learn to
# mimic x.

    # Variables: x, y

# Public:

    def calc_vel(ps):
        return (0.0, 0.0)

# `window` may be None, but this prevents interrupting learning.
def learn(population, world, window, BallInputType):

    sim = Simulator(world, window, False, True)
    mine_input = UniformMineInput()

    if population is None:
        # Fill population with blue noise, using stippling for tabu search.
        population = get_blue_noise_on_L1_sphere(population_size, chromosome_len)
    # Even population size is useful because crossover produces two chromosomes.
    # population_size = len(population)
    assert(len(population) % 2 == 0)

    fitnesses = []
    generation = 0

    while generation <= 5 and max(fitnesses) < 30.0:
        generation += 1

        fitnesses = calc_fitnesses(fitnesses, population, sim, mine_input, BallInputType)
        if fitnesses is None:
            break

        # operation_num = crossover_num + mutation_num + reproduction_num
        # len(population)/2 <= operation_num <= len(population)
        op_nums = get_op_nums(len(population), crossover_pr, mutation_pr)

        # Selection from existing population can be done in parallel.
        # len(selected) can be determined in one pass over `operations`.
        # len(population)/2 <= len(selected) <= len(population)
        selection_num = selection_num_from_op_nums(op_nums)
        selective_pressure = 2.0
        selected = select_chromosomes(selection_num, selective_pressure, fitnesses)

        # Operations can also be performed in parallel. The index of
        # an operation shows the result's index in `new_population`.
        population = make_population(population, selected, op_nums)

    return population, fitnesses

if __name__ == __main__:
    world = get_simple_world()
    window = Window()
    learn(None, world, window, NeuralNetBallAI)