from vec import *

class Bitmap: # Everything is public. Only `bits` is mutable.

    def __init__(self, bits, size_in_bits, corner, step):
        
        self.size_in_bits = size_in_bits
        self.len = size_in_bits[0] * size_in_bits[1]
        
        if bits is None:
            self.bits = [False] * self.len
        else:
            assert(len(bits) == self.len)
            self.bits = bits

        self.size     = vec_scale(size_in_bits, step)
        self.corner   = corner
        self.step     = step
        self.inv_step = 1.0 / step # Multiplication is faster than division.

    def get_row_start_index(self, y):
        width_in_bits = self.size_in_bits[0]
        return y * width_in_bits

    def index_from_indices(self, indices):
        x = indices[0]
        y = indices[1]
        return self.get_row_start_index(y) + x

    def indices_from_pos(self, pos):
        translated = vec_sub(pos, self.corner)
        scaled     = vec_scale(translated, self.inv_step)
        return (int(scaled[0]), int(scaled[1]))
   
    def index_from_pos(self, pos):
        indices = self.indices_from_pos(pos)
        return self.index_from_indices(indices)

    def are_indices_in_bounds(self, indices):
        return (indices[0] >= 0 and indices[0] < self.size_in_bits[0] and
                indices[1] >= 0 and indices[1] < self.size_in_bits[1])

    def pos_from_indices(self, indices):
        unscaled     = vec_scale(indices, self.step)
        untranslated = vec_add(unscaled, self.corner)
        return untranslated

    def get_bit_corners(self, indices):
        # a = map(float, indices) # I wish CPython inlined things.
        a = (float(indices[0]), float(indices[1]))
        b = vec_add(a, (1.0, 1.0))
        return (a, b)

    def get_AABB_corners(self, indices):
        a = self.pos_from_indices(indices)
        b = vec_add(a, (self.step, self.step))
        return (a, b)

    def to_str(self, false_char, true_char):
        w, h = self.size_in_bits[0], self.size_in_bits[1]
        
        row_chars = [None] * w
        rows      = [None] * h

        char_set = (false_char, true_char)

        i = 0
        for y in range(h):
            for x in range(w):
                char_index = int(self.bits[i]) # int(False) == 0 and int(True) == 1
                row_chars[x] = char_set[char_index]
                i += 1
            rows[y] = ''.join(row_chars)
        assert(i == self.len)
        
        rows.reverse() # Bigger y coord means further down.
        return '\n'.join(rows)