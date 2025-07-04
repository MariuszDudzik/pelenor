
import kolor
import pygame


class ZoomHandler(object):
   
    @staticmethod
    def handleIn(get_camera, play_obj):
        camera = get_camera()
        if camera.getCameraScale() <= camera.getmaxScale():
            camera.setCameraScale(camera.getCameraScale() + 0.5)
            play_obj.setHexBaseSize()
            play_obj.setHexes()

    @staticmethod
    def handleOut(get_camera, play_obj):
        camera = get_camera()
        if camera.getCameraScale() > camera.getminScale():
            camera.setCameraScale(camera.getCameraScale() - 0.5)
            play_obj.setHexBaseSize()
            play_obj.setHexes()


    @staticmethod
    def onHover(button):
        button.colour = kolor.RGREY

    @staticmethod
    def unHover(button):
        button.colour = kolor.GREY


class ToolTipHandler(object):
    
    @staticmethod
    def onHover(button, get_toolTip, screen_width, state_field_width):
        height = button.getPositionY()
        max_line_width = screen_width * 0.1
        toolTip = get_toolTip()
        toolTip.setPositionX(screen_width - state_field_width - max_line_width - 10)
        toolTip.setPositionY(height)
        text = button.getText()
        toolTip.setTextWrapped(text, max_line_width)
       

    @staticmethod
    def unHover(button, play_obj):
        play_obj.map.setDirty()
        for hex_obj in play_obj.hex.values():
            hex_obj.setDirty()
  
        """
        dodac odzwiezazznie wojska jak bedzie gotowe"""
       
       