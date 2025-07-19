class Camera(object):

    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 15
        self.scale = 1.0
        self.zoom_speed = 0.05
        self.min_x = -2210
        self.min_y = -1570
        self.max_x = 0
        self.max_y = 0
        self.max_scale = 7.0
        self.min_scale = 1.0

    def set_min_x(self, x):
        self.min_x = x

    def set_min_y(self, y):
        self.min_y = y

    def get_max_scale(self):
        return self.max_scale

    def get_min_scale(self):
        return self.min_scale

    def get_min_x(self):
        return self.min_x

    def get_min_y(self):
        return self.min_y

    def get_max_x(self):
        return self.max_x

    def get_max_y(self):
        return self.max_y

    def set_camera_x(self, x):
        self.camera_x = x

    def set_camera_y(self, y):
        self.camera_y = y

    def set_camera_scale(self, scale):
        self.scale = scale

    def get_camera_x(self):
        return self.camera_x

    def get_camera_y(self):
        return self.camera_y

    def get_camera_scale(self):
        return self.scale

    def get_camera_speed(self):
        return self.camera_speed

    def get_zoom_speed(self):
        return self.zoom_speed
    
