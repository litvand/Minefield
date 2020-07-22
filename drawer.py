import math
sin = math.sin
cos = math.cos

import pyglet as pg
from pyglet.gl import *
from vec       import *
from mathutil  import *
from minemap   import *

def get_verts_around_diamond(pos, rad): # Fast but poor approximation to circles
    x = pos[0]
    y = pos[1]
    right = x + rad
    up    = y + rad
    left  = x - rad
    down  = y - rad
    return ((right, y), (x, up), (left, y), (x, down))

def get_verts_around_circle(pos, rad, vert_num):
    
    assert(vert_num > 0)
    assert(int(vert_num) == vert_num)
    
    step = 2.0 * math.pi / float(vert_num)
    angle = 0.0
    verts = []
    
    for i in range(vert_num):
        x = cos(angle)
        y = sin(angle)
        vert = vec_add(pos, vec_scale((x, y), rad))
        verts.append(vert)
        angle += step
    
    assert(is_about_equal(angle, 2.0 * math.pi, 0.00001))
    return verts
    
def unpack_verts(verts):
    unpacked = []
    for i in range(len(verts)):
        unpacked.extend(verts[i])
    return unpacked
    
class CircleLineList:
    def __init__(self):
        self.vert_list = pg.graphics.vertex_list(0, 'v2f/stream')
        
    def set_lines(self, poss, rad, seg_num_per_line):
        
        line_num = len(poss)
        vert_num_per_line = 2 * seg_num_per_line
        vert_num = line_num * vert_num_per_line
        coords = []
        
        for i in range(line_num):
            pos = poss[i]
            verts = get_verts_around_circle(pos, rad, seg_num_per_line)
            
            for i in range(len(verts) - 1):
                coords.extend(verts[i])
                coords.extend(verts[i + 1])
            coords.extend(verts[-1])
            coords.extend(verts[0])
        
        assert(len(coords) == 2 * vert_num)
        self.vert_list.resize(vert_num)
        self.vert_list.vertices = coords
    
    def draw(self):
        self.vert_list.draw(GL_LINES)
            
class CircleList: # TODO: Reduce code duplication (CircleLineList).
    def __init__(self):
        self.vert_list = pg.graphics.vertex_list(0, 'v2f/stream')

    def set_circles(self, poss, rad, triangle_num_per_circle):
        circle_num = len(poss)
        vert_num_per_circle = 3 * triangle_num_per_circle
        vert_num = circle_num * vert_num_per_circle
        coords = []
        
        for i in range(circle_num):
            pos = poss[i]
            verts = get_verts_around_circle(pos, rad, triangle_num_per_circle)
            
            for i in range(len(verts) - 1):
                coords.extend(verts[i])
                coords.extend(pos)
                coords.extend(verts[i + 1])
            coords.extend(verts[-1])
            coords.extend(pos)
            coords.extend(verts[0])
        
        assert(len(coords) == 2 * vert_num)
        self.vert_list.resize(vert_num)
        self.vert_list.vertices = coords

    def draw(self):
        self.vert_list.draw(GL_TRIANGLES)

def get_AABB_triangle_vert_coords(ax, ay, bx, by):
    return (ax, ay, # Triangle 1
            bx, ay,
            ax, by,
            
            bx, ay, # Triangle 2
            bx, by,
            ax, by)

class Mask:
    def __init__(self):
        self.vert_list = pg.graphics.vertex_list(0, 'v2f/stream')
    
    def set(self, corner, size, max_size): # `max_size` indicates the window's border.
        
        a = (0.0, 0.0)
        b = corner
        c = vec_add(corner, size)
        d = max_size
        
        aabbs = ((a, a, b, d), (b, a, c, b), (b, c, c, d), (c, a, d, d))
        all_coords = []
        for i in range(len(aabbs)):
            r = aabbs[i]
            coords = get_AABB_triangle_vert_coords(r[0][0], r[1][1], r[2][0], r[3][1])
            all_coords.extend(coords)
        
        coord_num_per_vert = 2
        vert_num_per_AABB  = 6
        num_of_AABBs       = 4
        total_vert_num  = vert_num_per_AABB  * num_of_AABBs
        total_coord_num = coord_num_per_vert * total_vert_num
        assert(len(all_coords) == total_coord_num)
        
        self.vert_list.resize(total_vert_num)
        self.vert_list.vertices = all_coords
    
    def draw(self):
        self.vert_list.draw(GL_TRIANGLES)

class BitmapDrawer:

    @staticmethod
    def get_AABB_coords(bitmap):
        coords = []
        w, h = bitmap.size_in_bits[0], bitmap.size_in_bits[1]
        bits = bitmap.bits
        i = 0
        for y in range(h):
            for x in range(w):
                if bits[i]:
                    indices = (x, y)
                    c = bitmap.get_AABB_corners(indices)
                    ax, ay, bx, by = c[0][0], c[0][1], c[1][0], c[1][1]
                    coords.extend(get_AABB_triangle_vert_coords(ax, ay, bx, by))
                i += 1
        return coords

    @staticmethod
    def get_grid_coords(bitmap):
        
        coords = []
        for i in range(2):
            
            small_index = 0
            large_index = bitmap.size_in_bits[i]
            
            for other in range(bitmap.size_in_bits[1 - i]):

                if i == 0:
                    small_indices = (small_index, other)
                    large_indices = (large_index, other)
                else:
                    small_indices = (other, small_index)
                    large_indices = (other, large_index)

                small_pos = bitmap.pos_from_indices(small_indices)
                large_pos = bitmap.pos_from_indices(large_indices)
                coords.extend(small_pos)
                coords.extend(large_pos)
        return coords

    @staticmethod
    def set_coords(vert_list, coords):
        assert(len(coords) % 2 == 0)
        vert_list.resize(int(len(coords) / 2))
        vert_list.vertices = coords

# Public:

    def __init__(self):
        self.grid_vert_list = pg.graphics.vertex_list(0, 'v2f/stream')
        self.aabb_vert_list = pg.graphics.vertex_list(0, 'v2f/stream')
    
    def set(self, bitmap):
        self.set_coords(self.aabb_vert_list, self.get_AABB_coords(bitmap))
        self.set_coords(self.grid_vert_list, self.get_grid_coords(bitmap))
    
    def draw(self):
        self.aabb_vert_list.draw(GL_TRIANGLES)
        glColor3f(0.5, 0.5, 0.5)
        self.grid_vert_list.draw(GL_LINES)
        
class Drawer: # TODO: wall, switches, goals, hives, HUD, spawn cost, explosions, clouds

    def draw_spawning(self, ps):
        glColor3f(0.5, 0.0, 0.0)
        poss = ps.get_spawner().get_poss()
        rad  = 0.5 * ps.get_mines().rad
        self.spawning_list.set_circles(poss, rad, 4)
        self.spawning_list.draw()
        
    def draw_mines(self, ps):
        glColor3f(1.0, 0.0, 0.0) # Deprecated OpenGL - use a uniform in C++.
        mines = ps.get_mines()
        self.mine_list.set_circles(mines.get_poss(), mines.rad, 6)
        self.mine_list.draw()

    def draw_balls(self, ps):
        
        balls = ps.get_balls()
        poss = balls.get_poss()
        
        glColor3f(0.0, 0.0, 1.0)
        self.ball_list.set_circles(poss, balls.rad, 6)        
        self.ball_list.draw()
        
        force_field_min_rad = ps.get_spawner().min_ball_added_mine_dist
        if self.show_force_field_min:
            glColor3f(0.0, 0.0, 0.5)
            self.force_field_list.set_lines(poss, force_field_min_rad, 32)
            self.force_field_list.draw()
        
        if self.show_force_field_max:
            glColor3f(0.0, 0.0, 0.5)
            force_field_max_rad = force_field_min_rad + ps.get_spawner().full_power_level
            self.force_field_list.set_lines(poss, force_field_max_rad, 32)
            self.force_field_list.draw()
        
        if self.show_mine_bitmap_size: # For debugging
            glColor3f(0.5, 0.0, 0.0)
            bitmap_rad = mine_bitmap_side_len * balls.rad * 0.5
            self.force_field_list.set_lines(poss, bitmap_rad, 16)
            self.force_field_list.draw()
    
    def draw_mine_bitmap(self, bitmap):
        glColor3f(1.0, 0.0, 0.0)
        self.bitmap_drawer.set(bitmap)
        self.bitmap_drawer.draw()

    def draw_mask(self, corner, size, ps):

        wall = ps.get_wall()
        max_size = (wall.width, wall.height)
        
        glColor3f(0.0, 0.0, 0.0)
        self.mask.set(corner, size, max_size)
        self.mask.draw()
    
    def maybe_draw_mine_bitmap(self, ball_index, ps):

        ball_poss = ps.get_balls().get_poss()
        if ball_index >= len(ball_poss):
            return

        bitmap = get_mine_bitmap(ball_index, ps)
        self.draw_mine_bitmap(bitmap)
        #self.draw_mask(bitmap.corner, bitmap.size, ps)

    def set_notice_text(self, text):
        if self.notice.text != text:
            self.notice.begin_update()
            self.notice.text = text
            self.notice.end_update()

    def draw_notice(self, ps, is_paused):
        text = str(ps.get_mines().get_del_num()) + '  '
        if is_paused:
            text = text + 'P'
        if ps.get_balls().are_invincible():
            text = text + 'I'
        spawner = ps.get_spawner()
        percent = int(100 * spawner.get_add_power_level() / spawner.full_power_level)
        self.set_notice_text(text + '  ' + str(percent))
        self.notice.draw()

# Public:

    def reset(self):
        self.set_notice_text('')

    def __init__(self, window, draw_fps = True):
        
        self.show_force_field_min  = True
        self.show_force_field_max  = True
        self.show_mine_bitmap_size = False
        
        self.window = window
        glClearColor(0.46, 0.7, 0.86, 1.0)
        
        self.spawning_list = CircleList()
        self.mine_list = CircleList()
        self.ball_list = CircleList()
        self.force_field_list = CircleLineList()
        
        self.bitmap_drawer = BitmapDrawer()
        self.mask = Mask()
        
        self.fps_display = pg.clock.ClockDisplay() if draw_fps else None
        self.notice = pg.text.Label(
            '', font_name = 'Courier New', font_size = 12,
            x = 5.0, y = window.height - 5.0, anchor_x = 'left', anchor_y = 'top'
        )

    def draw(self, ps, is_paused):
        self.window.clear()
        self.draw_spawning(ps)
        #self.draw_mines(ps)
        self.draw_balls(ps)
        self.maybe_draw_mine_bitmap(0, ps)
        self.draw_notice(ps, is_paused)
        if self.fps_display is not None:
            self.fps_display.draw()
