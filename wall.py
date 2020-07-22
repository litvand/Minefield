from vec import *

class Wall:

    def are_row_rect_spans_valid(self, row):
        # Spans are inclusive.
        for j in range(len(row)):
            if row[j][0] > row[j][1]:
                return False
            for k in range(2):
                if row[j][k] < 0 or row[j][k] >= self.width_in_tiles:
                    return False
        return True

    def get_row_rect_spans(self, row_start): # `row_start` is inclusive.

        is_wall = self.bitmap
        row_end = row_start + self.width_in_tiles # Exclusive

        rect_start = None

        row = []
        for j in range(row_start, row_end):
            # assert(j >= 0)
            # assert(j < len(is_wall))
            if is_wall[j]:
                if rect_start is None:
                    rect_start = j
            elif rect_start is not None:
                rect_last = j - 1
                row.append((rect_start, rect_last))
                rect_start = None

        if rect_start is not None: # One left over touching the right edge
            row.append((rect_start, row_end - 1))

        assert(self.are_row_rect_spans_valid(row))
        return row

    def get_rect_spans(self):
        w, h = self.width_in_tiles, self.height_in_tiles

        rows = [] # Fill `rows` with rectangles for each row.
        row_start = 0 # Inclusive

        for i in range(h):
            rows.append(self.get_row_rect_spans(row_start))
            row_start += w
        assert(row_start == w * h)
        return rows

    def update_rects(self):

        spans = self.get_rect_spans()
        self.rects = []

        # TODO: Merge rectangles on adjacent rows
        # with equal start and end x coordinates.

        for i in range(len(spans)):
            row = spans[i]
            for j in range(len(row)):
                span = row[j]
                ax, bx = span[0], 1 + span[1]
                ay, by = i,       1 + i
                self.rects.append((ax, ay, bx, by))

        self.update_num += 1

    # TODO: Store and update rects in drawer.
    # TODO: Also maintain polygons, shortest path data structures?

# Public:

    def reset(self, initial_bitmap):
        self.updating = True
        self.bitmap = list(initial_bitmap)
        self.update_rects()
        self.update_num += 1
        self.updating = False

    def __init__(self, world):

        # Constants:
        self.height_in_tiles = world.height_in_tiles
        self.width_in_tiles  = world.width_in_tiles
        self.tile_width      = world.tile_width
        self.tile_height     = world.tile_height
        self.width  = world.width
        self.height = world.height

        # Variables:
        self.update_num = 0 # unsigned int (overflow not undefined)

        self.reset(world.initial_wall_bitmap)

    def begin_bitmap_update(self):
        assert(not self.updating)
        self.updating = True
        return self.bitmap # Not const

    def finish_bitmap_update(self, bitmap):
        assert(self.updating)
        # assert(&(self.bitmap) == &bitmap) # Pointer comparison
        self.update_rects()
        self.update_num += 1
        self.updating = False

    def get_update_num(self):
        return self.update_num

    def get_bitmap(self):
        assert(not self.updating)
        return self.bitmap

    def get_rects(self):
        assert(not self.updating)
        return self.rects

    def is_circle_within_borders(self, pos, rad): # TODO
        return True

    def is_circle_collision(self, pos, rad): # TODO
        return False

    def is_visible(self, a, b): # TODO
        return True

    def is_circle_visible(self, point, center, rad): # TODO
        return True

    def adjust_step(self, pos, rad, old_step): # TODO: non-border walls

        new_pos = vec_add(pos, old_step)
        sx = old_step[0]
        sy = old_step[1]

        too_small_x = (sx < 0.0 and new_pos[0] <= rad)
        too_big_x   = (sx > 0.0 and new_pos[0] >= self.width - rad)
        if too_small_x or too_big_x:
            sx = 0.0

        too_small_y = (sy < 0.0 and new_pos[1] <= rad)
        too_big_y   = (sy > 0.0 and new_pos[1] >= self.height - rad)
        if too_small_y or too_big_y:
            sy = 0.0

        return (sx, sy)
