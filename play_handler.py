
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
    def onHover(button, get_toolTip, toolX, toolY, max_line_width):
        toolTip = get_toolTip()
        toolTip.setPositionX(toolX)
        toolTip.setPositionY(toolY)
        text = button.getTipText()
        toolTip.setTextWrapped(text, max_line_width)


    @staticmethod
    def unHover(button, play_obj):
        play_obj.map.setDirty()
        for hex_obj in play_obj.hex.values():
            hex_obj.setDirty()
  
        """
        dodac odzwiezazznie wojska jak bedzie gotowe"""


    @staticmethod
    def onHoverReinforcement(button, get_toolTip, toolX, toolY, max_line_width):
        if button.unit.getSite() == 'Z':
            button.setColour(kolor.RLIME)
        elif button.unit.getSite() == 'C':
            button.setColour(kolor.RREDJ)
        ToolTipHandler.onHover(button, get_toolTip, toolX, toolY, max_line_width)


    @staticmethod
    def unHoverReinforcement(button, play_obj):
        if button.unit.getSite() == 'Z':
            button.setColour(kolor.LIME)
        elif button.unit.getSite() == 'C':
            button.setColour(kolor.REDJ)
        for sprite in play_obj.leftMenuGraphics.sprites():
            sprite.setDirty()
      
       
       