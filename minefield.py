# Abbreviations:

# coord - coordinate
# pr    - probability
# prs   - probabilities
# tgt   - target
# pos   - position
# poss  - positions
# vel   - velocity
# del   - delete
# inv   - inverse
# vec   - vector
# AABB  - axis-aligned bounding box
# rad   - radius
# rect  - rectangle
# circ  - circle
# dist  - distance
# sqr   - square
# calc  - calculate
# eps   - epsilon (small error)
# dim   - dimension
# rand  - random
# exp   - exponent, exponential
# cur   - current
# op    - operation
# vert  - vertex
# gen   - generator, generate
# buf   - buffer
# elem  - element
# param - parameter
# diff  - difference
# inc   - increment
# dec   - decrement
# prev  - previous
# seg   - segment

# Conventions:

# `get*` methods return const variables and do not mutate `self`.

# `try*` functions return either False or None on failure.
# Functions that return False on failure will return True on success.
# Functions that return None on failure will return a
# non-boolean value `v` on success, such that `not v` is False.

# `maybe*` functions are like `try*` functions, but
# do not have to return anything.

# Only const members can be public, unless all members are public (struct).

# Member variables should only be initialized in constructors.

from play import play

# Errors when stress testing with 500-1000 mines (300-400 MB used, with spikes to 700 MB):
# AllocatorMemoryException in allocator.realloc (vertexdomain.py): 33555900
# GLException in vert_list.resize: 'out of memory'
# AssertionError twice in ps.advance: assert(self.can_mutate)

# Next time stress testing with up to 1552 mines (1684 deleted) for
# 107.95 seconds gave no errors, though fps dropped to about 1.5.

# Bug in pyglet?

play()