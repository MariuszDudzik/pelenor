class Camera(object):

    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 30
        self.scale = 1.0
        self.zoom_speed = 0.07

    def setCameraX(self, x):
        self.camera_x = x

    def setCameraY(self, y):
        self.camera_y = y
    
    def setCameraScale(self, scale):
        self.scale = scale

    def getCameraX(self):
        return self.camera_x
    
    def getCameraY(self):
        return self.camera_y
    
    def getCameraScale(self):
        return self.scale
    
    def getCameraSpeed(self):
        return self.camera_speed
    
    def getZoomSpeed(self):
        return self.zoom_speed
