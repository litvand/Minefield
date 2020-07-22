import ringbuf

class Cloud: # Just a struct
    def __init__(self, width, height, vel):
        self.height = height
        self.width  = width
        self.vel = vel

def is_positive_span(span):
    return len(span) == 2 and span[0] > 0.0 and span[1] >= span[0]

def get_rand_in_span(span):
    return random.uniform(span[0], span[1])

class Clouds:

    def make_cloud(self):
        height = get_rand_in_span(self.height_span)
        width  = get_rand_in_span(self.width_span)
        vel    = get_rand_in_span(self.vel_span)
        return Cloud(width, height, vel)

    def add_cloud(self):
        self.clouds.add(self.make_cloud())
        # Update next cloud time.

# Public:

    def reset(self):
        self.total_added_num = 0
        self.clouds.reset()
        self.add_times = [] # When a cloud was added to clouds (x coord = 0)
        self.next_add_time = 0.0

    def __init__(self, world_height): # TODO

        # Constants:
        self.height_span = height_span
        self.width_span  = width_span
        self.vel_span    = vel_span
        self.max_cloud_num = max_cloud_num
        self.clouds = RingBuf(self.max_cloud_num) # RingBuf<Cloud>  ?

        assert(height_span[1] < world_height) # TODO: Move into World constructor?
        assert(is_positive_span(height_span))
        assert(is_positive_span(width_span))
        assert(is_positive_span(vel_span))

        self.reset()

    def get_total_num(self): # Total number of clouds created by this object
        return self.total_added_num

    def get_cur_num(self):
        return self.clouds.len()

    def advance(self, dt):
        pass
