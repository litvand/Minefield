import pyglet as pg
import pyglet.window.key as keys

class Window:   # Could be implemented using a glfwWindow, for example.

    def try_make_window_from_template(self, width, height, template): # static function

        platform = pg.window.get_platform() # Pyglet singleton
        display  = platform.get_default_display()
        screen   =  display.get_default_screen()

        config = None
        try:
            config = screen.get_best_config(template)
        except pg.window.NoSuchConfigException as e:
            print("Couldn't use this pyglet window config:")
            print(e)
            return None

        return pg.window.Window(width, height, config = config)

    def try_make_window(self, width, height): # static function
        return self.try_make_window_from_template(width, height, pg.gl.Config())

# Public:

    def __init__(self, width, height):

        self.w = self.try_make_window(width, height)
        assert(self.w) # TODO: throw something (RuntimeError?)

        self.width  = width
        self.height = height

        self.key_state_handler = keys.KeyStateHandler()
        self.w.push_handlers(self.key_state_handler)

        self.update_func = None

        cursor = self.w.get_system_mouse_cursor('crosshair')
        self.w.set_mouse_cursor(cursor)

    def on_draw(self, draw_func):
        self.w.on_draw = draw_func

    def on_update(self, update_func, fps = None): # TODO: Replace `fps` with `dt`?

        if self.update_func is not None:
            pg.clock.unschedule(self.update_func)
        self.update_func = update_func

        if update_func is not None:
            assert(fps is not None)
            pg.clock.schedule_interval(update_func, 1.0 / float(fps))

    def on_scroll(self, scroll_func):
        self.w.on_mouse_scroll = scroll_func

    def on_click(self, click_func):
        self.w.on_mouse_press = click_func

    def clear(self):
        self.w.clear()

    def run(self):
        pg.app.run()

    def close(self):
        self.w.close()

    def is_pressed(self, key):
        return self.key_state_handler[key]