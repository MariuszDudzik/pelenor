

class ZoomInHandler(object):
    @staticmethod
    def handle(camera):
       camera.setCameraScale(min(1.85, camera.getCameraScale() + camera.getZoomSpeed()))

class ZoomOutHandler(object):
    @staticmethod
    def handle(camera):
        camera.setCameraScale(max(1, camera.getCameraScale() - camera.getZoomSpeed()))
                       