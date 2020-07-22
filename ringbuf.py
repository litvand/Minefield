
class RingBuf:

    def reset(self, max_len=None):
        if max_len is None:
            max_len = self.list.len()
        assert(max_len > 0)
        self.list = [None] * max_len
        self.insert_pos = 0
        self.cur_len = 0

    def __init__(self, max_len):
        self.reset(max_len)

    def max_len(self):
        return self.list.len()

    def len(self):
        return self.cur_len

    def is_free_space(self):
        return self.len() < self.max_len()

    def elems(self):    # Allow modifying elems without allowing resizing list.
        return self.list

    def elem(self, num_elems_added_later): # 0 for most recent element

        assert(num_elems_added_later >= 0)

        max_len = self.max_len()
        if num_elems_added_later >= max_len:
            return None # TODO: assert(num_elems_added_later < max_len) instead?

        index = self.insert_pos - num_elems_added_later
        if index < 0:
            index += max_len
        elif index >= max_len:
            index -= max_len
        assert(index >= 0)
        assert(index < max_len)

        return self.list[index]

    def add(self, elem):
        self.list[self.insert_pos] = elem
        self.insert_pos = (self.insert_pos + 1) % self.max_len()
        self.cur_len = min(self.cur_len + 1, self.max_len())
