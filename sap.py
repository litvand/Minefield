from vec import *

class CircleSAP: # Sweep and prune

    @staticmethod
    def is_index_list(the_list):
        for i in range(len(the_list)):
            x = the_list[i]
            if int(x) != x or x < 0 or x >= len(the_list):
                return False
        return True

    @staticmethod
    def expand_index_list(new_len, the_list):

        cur_len = len(the_list)
        assert(new_len > cur_len)

        new_indices = range(cur_len, new_len)
        the_list.extend(new_indices)

        assert(len(the_list) == new_len)

    def expand(self, new_len):
        self.expand_index_list(new_len, self.indices)

    @staticmethod
    def shrink_index_list(new_len, the_list):

        assert(new_len >= 0)

        # Copy elements we need from the end to the middle
        # of the list, overwriting elements we don't need.
        for i in range(len(the_list) - 1, -1, -1):
            if the_list[i] >= new_len:
                the_list[i] = the_list[-1]
                del the_list[-1]

        assert(len(the_list) == new_len)

    def shrink(self, new_len):
        self.shrink_index_list(new_len, self.indices)

    def resize(self, new_len):
        cur_len = len(self.indices)
        if new_len > cur_len:
            self.expand(new_len)
        elif new_len < cur_len:
            self.shrink(new_len)
        assert(self.is_index_list(self.indices))

# Public:

    def __init__(self):
        self.indices = [] # (partially sorted) indices of circle positions

    def find_collisions(self, poss, has_collided, rad): # Mutates `has_collided`.
        # Doesn't mutate `poss` (or `rad`).

        assert(rad > 0.0)

        circle_num = len(poss)
        assert(len(has_collided) == circle_num)
        self.resize(circle_num)

        coord_index = 0 # Controls which coordinate to sort and prune by.
        self.indices.sort(key = lambda index: poss[index][coord_index])

        # Meta-index = index in `indices`
        last = 0              # Meta-index of last circle to test collision with.
        min_dist = 2.0 * rad
        # If the distance along some axis is less than
        # `min_dist`, there might be a collision.
        min_sqr_dist = min_dist * min_dist # For actual collision test

        for meta_index_a in range(circle_num - 1):

            index_a = self.indices[meta_index_a]
            pos_a   = poss[index_a]

            # Update `last`.
            max_last_coord = pos_a[coord_index] + min_dist
            while last < circle_num - 1:
                next = last + 1
                coord = poss[self.indices[next]][coord_index]
                if coord >= max_last_coord:
                    break
                last = next

            # Test actual collisions.
            range_end = last + 1
            # collision_test_num += range_end - meta_index_a
            for meta_index_b in range(meta_index_a + 1, range_end):
                index_b = self.indices[meta_index_b]
                pos_b   = poss[index_b]
                sqr_dist = vec_sqr_dist(pos_a, pos_b)
                is_collision = (sqr_dist <= min_sqr_dist)
                has_collided[index_a] = has_collided[index_a] or is_collision
                has_collided[index_b] = has_collided[index_b] or is_collision
