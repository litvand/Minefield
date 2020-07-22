from wall import Wall

class World: # Just contains all level data.

    # TODO: Nicer constructor?
    def __init__(self, initial_wall_bitmap,
                 mine_max_speed, mine_rad, are_mines_magnetic,
                 ball_max_speed, ball_rad, initial_ball_poss,
                 width_in_tiles, height_in_tiles, tile_width, tile_height,
                 power_fill_speed, full_power_level, explosive_power_level,
                 min_spawn_time, max_spawn_time, min_ball_added_mine_dist):

        self.initial_wall_bitmap = initial_wall_bitmap

        self.mine_max_speed     = mine_max_speed
        self.mine_rad           = mine_rad
        self.are_mines_magnetic = are_mines_magnetic

        self.ball_max_speed     = ball_max_speed
        self.ball_rad           = ball_rad
        self.initial_ball_poss  = initial_ball_poss

        self.width_in_tiles     = width_in_tiles
        self.height_in_tiles    = height_in_tiles
        self.tile_width         = tile_width
        self.tile_height        = tile_height

        self.width  =  width_in_tiles * tile_width
        self.height = height_in_tiles * tile_height

        self.power_fill_speed      = power_fill_speed
        self.full_power_level      = full_power_level
        self.explosive_power_level = explosive_power_level
        self.min_spawn_time        = min_spawn_time
        self.max_spawn_time        = max_spawn_time
        self.min_ball_added_mine_dist = min_ball_added_mine_dist

        assert(self.min_ball_added_mine_dist > 0.0)
        assert(self.min_spawn_time > 0.0)
        assert(self.min_spawn_time <= self.max_spawn_time)
        assert(self.power_fill_speed > 0.0)
        assert(self.full_power_level > 0.0)
        assert(self.explosive_power_level is None or
               self.explosive_power_level >= self.full_power_level)

        area_in_tiles = width_in_tiles * height_in_tiles
        assert(len(initial_wall_bitmap) == area_in_tiles)
        assert(width_in_tiles  > 0)
        assert(height_in_tiles > 0)
        assert(tile_width  > 0.0)
        assert(tile_height > 0.0)
        assert(mine_max_speed > 0.0)
        assert(ball_max_speed > 0.0)
        assert(mine_rad > 0.0)
        assert(ball_rad > 0.0)

        wall = Wall(self)
        for i in range(len(initial_ball_poss)):
            pos = initial_ball_poss[i]
            assert(wall.is_circle_within_borders(pos, ball_rad)) # REM?
            assert(not wall.is_circle_collision(pos, ball_rad))
