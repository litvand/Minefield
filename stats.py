def get_rand_samples(sample_num, weights): # Stochastic universal sampling [Bak87]
    # Returns indices into weights. There may duplicate
    # indices in `selected`, but they will be adjacent.
    # For example:
    # selected = [0, 1, 1, 3, 4, 4, 4, 5, 7, 8]
    # sample_num == 10 and len(weights) >= 9

    # Time complexity: Theta(max(sample_num, len(weights))).

    partial_sums = get_partial_sums(weights)
    assert(len(partial_sums) == len(weights))
    sum_of_all_weights = partial_sums[-1]
    step = sum_of_all_weights / float(sample_num)

    cur_index = 0
    cur_point = get_uniform_rand(0.0, step)

    selected = []
    for i in range(sample_num):
        while (cur_index + 1 < len(weights)) and (cur_point > partial_sums[cur_index]):
            cur_index += 1
        assert(cur_index >= 0)
        assert(cur_index < len(weights))
        selected.append(cur_index)
        cur_point += step
    assert(len(selected) == sample_num)
    return selected

def has_unit_sum(vec): # Sum of coords is about 1.
    return is_about_equal(fsum(vec), 1.0, 0.000001) # TODO: Adjust eps.

def are_in_unit_range(vec): # Each coordinate is in the range [0; 1].
    for i in range(len(vec)):
        x = vec[i]
        if x < 0.0 or x > 1.0:
            return False
    return True

def is_on_unit_simplex(vec):
    return are_in_unit_range(vec) and has_unit_sum(vec)

def kraemer_algorithm(dim_num): # Alternate `get_uniform_rand_on_unit_simplex`
    a = []
    a.append(0.0)
    for i in range(dim_num - 1):
        a.append(get_uniform_rand(0.0, 1.0))
    a.append(1.0)
    a.sort()

    r = []
    for i in range(len(a) - 1):
        r.append(a[i + 1] - a[i])
    return r

def get_unit_exp_rand(dim_num):
    r = []
    for i in range(dim_num):
        uniform = get_uniform_rand(0.0, 1.0)
        assert(uniform != 1.0)  # Range should be [0; 1).
        flipped = 1.0 - uniform # Make range (0; 1].
        r[i] = -log(flipped)    # log(0) == -inf
    return r

def get_uniform_rand_on_unit_simplex(dim_num):
    r = get_unit_exp_rand(dim_num)
    s = 1.0 / fsum(r)
    for i in range(len(r)):
        r[i] *= s

    assert(len(r) == dim_num)
    assert(is_on_unit_simplex(r))
    return r