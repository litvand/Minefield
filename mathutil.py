import random
import math
sqrt = math.sqrt

def get_uniform_rand(min_val, max_val): # Guaranteed range [min_val; max_val)
    while True:
        u = random.uniform(min_val, max_val)
        if u != max_val:
            return u

def is_about_equal(a, b, eps):  # a = (b +- eps)
    return ((b - eps) <= a) and (a <= (b + eps))

def reciprocal(x):
    return 1.0 / x

def inv_sqrt(x):
    return 1.0 / sqrt(x)

def clamp(x, min_val, max_val):
    return min(max(x, min_val), max_val)

def is_within(x, min_val, max_val): # Inclusive range
    return clamp(x) == x

class Sum:
    def __init__(self, initial_sum = 0.0):
        self.sum = initial_sum

    def add(self, to_add):
        self.sum += to_add

    def get(self):
        return self.sum

class KahanSum: # Only people with short names should invent algorithms.
    def __init__(self, initial_sum = 0.0):
        self.sum = initial_sum
        self.compensation = 0.0

    def add(self, to_add):
        to_add -= self.compensation
        new_sum = self.sum + to_add
        self.compensation = (new_sum - self.sum) - to_add
        self.sum = new_sum

    def get(self):
        return self.sum

def kahan_sum(numbers): # Less accurate but (in C++) faster alternative to `fsum`
    sum = KahanSum()
    for i in range(len(numbers)):
        sum.add(numbers[i])
    return sum.get()

def get_partial_sums(numbers, SumType = KahanSum):
    cur_sum = SumType()
    sums = []
    for i in range(len(numbers)):
        cur_sum.add(numbers[i])
        sums.append(cur_sum.get())
    return sums
