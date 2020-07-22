# Normalized weights are points on an L1 norm unit sphere.

# Assume all L1 spheres are centered at the origin and
# have radius 1, unless stated otherwise.

def is_on_L1_sphere(vec):
    return is_on_unit_simplex(map(abs, vec))

def get_uniform_rand_on_L1_sphere(dim_num):
    # The sum of the coords' absolute values is equal to 1.
    # The absolute value of each weight is less than or
    # equal to 1.

    r = get_uniform_rand_on_unit_simplex(dim_num)
    for i in range(dim_num):

        # if random.getrandbits(1): # `not int(0)` is True in Python.
        #     r[i] = -r[i]

        # Branchless (XOR or OR sign bit in C++):
        sgn = -1 + (random.getrandbits(1) * 2)
        assert(sgn == -1 or sgn == 1)
        r[i] *= sgn

    assert(is_on_L1_sphere(r))
    return r

def get_L1_sphere_contact_params(a, b):
    assert(False) # TODO
    assert(is_on_L1_sphere(a))
    assert(is_on_L1_sphere(b))

def get_shortest_path_on_L1_sphere(a, b, c1, c2):

    d = vec_sub(b, a)
    n = len(a) # Number of dimensions

    # Find intersections with axis hyperplanes in `n - 1` dimensions.
    # Intersections are params `s` such that some coordinate of `a + (s * d)`
    # is equal to 0 and c1 < s < c2. Sort the intersections. Construct the
    # path from the intersections, with additional `n`-th dimensional
    # coordinates, and `a` and `b`. If the `n`-th coordinates of `a` and `b`
    # have different signs, the path may contain some pairs of points
    # differing only by the signs of their `n`-th coordinates (in addition
    # to `a` and `b`).

    # The path follows a straight `n`-th dimensional line between adjacent
    # points in the returned list. The straight lines between non-adjacent
    # points leave the surface of the L1 sphere.

    assert(False) # TODO

def get_dist_on_L1_sphere(a, b):
    # d = vec_sub(b, a) # REM
    c1, c2 = get_L1_sphere_contact_params(a, b)
    points = get_shortest_path_on_L1_sphere(a, b, c1, c2)
    dists = []
    for i in range(len(points) - 1):
        # The points are guaranteed to be connected by
        # straight line segments on the surface of the
        # L1 sphere, so we can just calculate the usual
        # Euclidean distance between them.
        dists.append(vec_dist(points[i], points[i + 1]))
    return sum(dists) # Use `kahan_sum` or `fsum` for more accuracy.

def mix_on_L1_sphere(a, b, s): # For use with simulated binary crossover
    # `s` is the interpolation/extrapolaton parameter.
    # `s` may be negative or greater than 1.0, but it will
    # wrap around if too large or too small (like angles).

    assert(False) # TODO

    c1, c2 = get_L1_sphere_contact_params(a, b)
    # if s == 0.0: return a
    # if s == 0.5: return average_on_L1_sphere(a, b, c1, c2)
    # if s == 1.0: return b

# genetic algorithm

def crossover_on_L1_sphere(a, b): # SBX

    assert(False) # TODO

    # Sample `beta` from custom probability distribution.
    # Use `beta` to calculate the third parameter to `mix`.
    # return mix_on_L1_sphere(a, b, something)

def get_blue_noise_on_L1_sphere(sample_num, dim_num):
    # Uses Poisson disk sampling on the surface of a `dim_num`-dimensional
    # unit L1 norm sphere to sample blue noise. Returns a list of `sample_num`
    # lists, each with `dim_num` numbers.

    # TODO: Take additional parameters (such as previous solutions)
    #       so tabu search can be used.

    assert(False) # TODO
