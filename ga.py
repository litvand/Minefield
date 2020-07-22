import l1
import stats

# Template (or macro) of BallInputType in C++
# Mutates `fitnesses`.
def calc_fitnesses(fitnesses, population, sim, mine_input, BallInputType):

    # Extend fitnesses with None so that len(fitnesses) >= len(population).
    len_diff = len(population) - len(fitnesses)
    if len_diff > 0:
        fitnesses.extend([None] * len_diff)

    for i in range(population): # Can be done in parallel (duplicate sim, mine_input).
        ball_input = BallInputType(population[i])
        sim.reset()
        sim.run(mine_input, (ball_input,))
        if sim.was_interrupted():
            sim.reset()
            return None
        fitnesses[i] = sim.get_elapsed_time()

    sim.reset()
    return fitnesses

def selection_num_from_op_nums(op_nums):
    c, m, r = op_nums
    return (m + r) + (2 * c) # Only crossover requires two input chromosomes.

def population_size_from_op_nums(op_nums):
    c, m, r = op_nums
    return r + (2 * (c + m)) # Only reproduction generates one chromosome.

def get_op_nums(population_size, crossover_pr, mutation_pr):
    # Derived from stochastic universal sampling
    assert(False) # TODO

    cp, mp = crossover_pr, mutation_pr
    assert(is_in_unit_range((cp, mp, cp + mp)))

    new_population_size = population_size
    assert(population_size_from_op_nums(op_nums) == new_population_size)

    return op_nums

def is_rank_selective_pressure_in_range(pressure, max_pressure):
    return pressure >= 1.0 and pressure <= max_pressure

def linear_weights_from_ranks(ranks, selective_pressure):
    # A rank is a zero-based index into the sorted list `fitnesses`.
    # weight = (2 - sp) + (2 * (sp - 1) * rank / (population_size - 1))
    sp = selective_pressure
    assert(is_rank_selective_pressure_in_range(sp, 2))
    population_size = len(ranks)
    a = (2.0 - sp)
    b = (2.0 * (sp - 1.0) / float(population_size - 1))
    weights = []
    for i in range(len(ranks)):
        weights.append(a + b * float(ranks[i]))
    return weights

def exp_weight_from_rank(rank, selective_pressure, population_size):
    assert(False) # TODO
    sp = selective_pressure
    assert(is_rank_selective_pressure_in_range(sp, population_size - 2))

def ranks_from_fitnesses(fitnesses):
    # TODO: Can ranks be calculated without using a
    #       temporary O(n) len list like `indices`?
    indices = list(range(len(fitnesses)))
    indices.sort(key = lambda rank: fitnesses[rank])
    ranks = [None] * len(indices)
    for rank in range(len(indices)):
        ranks[indices[i]] = rank
    return ranks # Index of each fitness in sorted fitnesses list

def weights_from_fitnesses(fitnesses, weight_from_rank, selective_pressure): # REM
    population_size = len(fitnesses)
    f = lambda rank: weight_from_rank(rank, selective_pressure, population_size)
    return map(f, ranks_from_fitnesses(fitnesses))

def select_chromosomes(selection_num, selective_pressure, fitnesses): # Returns indices.
    ranks = ranks_from_fitnesses(fitnesses)
    weights = linear_weights_from_ranks(ranks, selective_pressure)
    selected = get_rand_samples(selection_num, weights)
    return selected

def crossover(parent_chromosomes):
    assert(False) # TODO
    a, b = parent_chromosomes
    children = (a, b)
    return children

def get_uniform_random_chromosome():
    assert(False) # TODO

def mutate(chromosome):
    return crossover(chromosome, get_uniform_random_chromosome())

def reproduce(chromosome):
    return chromosome

def get_crossover_parents(population, selected, selection_index):
    i = selection_index
    p = population
    s = selected
    assert(i + 1 < len(s))
    return p[s[i]], p[s[i + 1]]

def make_population(population, selected, op_nums):

    c, m, r = op_nums
    j = 0
    new_population = []

    for i in range(c):
        new_population.extend(crossover(get_crossover_parents(population, selected, j)))
        j += 2

    for i in range(m):
        assert(j < len(selected))
        new_population.append(mutate(population[selected[j]]))
        j += 1

    for i in range(j, len(selected)):
        new_population.append(reproduce(population[selected[i]]))
    assert(r == len(selected) - j + 1) # All selected chromosomes were used up.

    return new_population
