class Camera(object):

    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 30
        self.scale = 1.0
        self.zoom_speed = 0.007
        self.minX = -2210
        self.minY = -1570
        self.maxX = 0
        self.maxY = 0
        self.maxScale = 7.0
        self.minScale = 1.0

    def setMinX(self, x):
        self.minX = x

    def setMinY(self, y):
        self.minY = y

    def getmaxScale(self):
        return self.maxScale
    
    def getminScale(self):
        return self.minScale

    def getMinX(self):
        return self.minX
    
    def getMinY(self):
        return self.minY
    
    def getMaxX(self):
        return self.maxX
    
    def getMaxY(self):
        return self.maxY

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
    
