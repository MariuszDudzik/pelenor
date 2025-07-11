
import kolor
import pygame
import gamelogic


class ZoomHandler(object):
   
    @staticmethod
    def handleIn(get_camera, play_obj):
        camera = get_camera()
        if camera.getCameraScale() <= camera.getmaxScale():
            camera.setCameraScale(camera.getCameraScale() + 0.5)
            play_obj.setHexBaseSize()
            play_obj.setMapView()

    @staticmethod
    def handleOut(get_camera, play_obj):
        camera = get_camera()
        if camera.getCameraScale() > camera.getminScale():
            camera.setCameraScale(camera.getCameraScale() - 0.5)
            play_obj.setHexBaseSize()
            play_obj.setMapView()


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
        for unit in play_obj.units.values():
            unit.setDirty()
        #Refresh.refresh_under_tooltip(play_obj)

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


    @staticmethod
    def onHoverunit(button, get_toolTip, toolX, toolY, max_line_width, play_obj):
        qrs = button.unit.getQRS()
        unitList = play_obj.game.board.hexes[qrs].pawnGraphList
        l = len(unitList) - 1
        for idx, id in enumerate(unitList):
            if idx < l:
                play_obj.units[id].setVisible(0)
                
            
        if button.unit.getSite() == 'Z':
            button.setColour(kolor.RLIME)
        elif button.unit.getSite() == 'C':
            button.setColour(kolor.RREDJ)
        play_obj.units[unitList[l]].setDirty()
        ToolTipHandler.onHover(play_obj.units[unitList[l]], get_toolTip, toolX, toolY, max_line_width)


    @staticmethod
    def unHoverunit(button, play_obj):
        if button.unit.getSite() == 'Z':
            button.setColour(kolor.LIME)
        elif button.unit.getSite() == 'C':
            button.setColour(kolor.REDJ)
        qrs = button.unit.getQRS()
        unitList = play_obj.game.board.hexes[qrs].pawnGraphList
        for idx, id in enumerate(unitList):
                play_obj.units[id].setVisible(1)
        Refresh.refresh_under_tooltip(play_obj)
        for sprite in play_obj.mapView.sprites():
            sprite.setDirty()
        # Refresh.refreshRight(play_obj)


class Refresh(object):

    @staticmethod
    def refreshLogin(play_obj):
        play_obj.playerWlogin.setText(play_obj.game.playerW.login)
        play_obj.playerSlogin.setText(play_obj.game.playerS.login)
        play_obj.playerWlogin.setDirty()
        play_obj.playerSlogin.setDirty()

    @staticmethod
    def refreshRight(play_obj):
        x = play_obj.toolTip.getPositionX() + play_obj.toolTip.getWidth()
        x2 = play_obj.stateField.getPositionX()
        if x >= x2:
            play_obj.setRightMenuDirty()


    @staticmethod
    def refresh_under_tooltip(play_obj):
        tooltip_rect = play_obj.getToolTip().getRect()
        for hit_hex in PlayHandler.get_hexes_under_rect(tooltip_rect, play_obj.hex):
            play_obj.hex[hit_hex].setDirty()
            Refresh.refresh_unit_graphics_list(play_obj, hit_hex)


    @staticmethod
    def refresh_unit_graphics_list(play_obj, qrs):
        for unit in play_obj.game.board.hexes[qrs].pawnGraphList:
                        play_obj.units[unit].setDirty()
        

class PlayHandler(object):

    @staticmethod
    def get_hexes_under_rect(rect, hex_graphics_dict, sampling_step=5):
        
        hit_hexes = set()

        for x in range(rect.left, rect.right, sampling_step):
            for y in range(rect.top, rect.bottom, sampling_step):
                for hex_pos, hex_sprite in hex_graphics_dict.items():
                    if hex_sprite.rect.collidepoint(x, y):
                        hit_hexes.add(hex_pos)
        return hit_hexes
    

    @staticmethod
    def change_hex_colour(play_obj, flag, matching):
        for qrs in matching:
            Lhex = play_obj.game.board.hexes[tuple(qrs)]
            Lhex.setColourFlag(flag)
            if qrs in play_obj.hex:
                hex_tile = play_obj.hex[qrs]
                colour = Lhex.getColour() if flag else Lhex.getDarkColour()
                hex_tile.setFillColour(kolor.colour_hex.get(colour))
                hex_tile.setDirty()
                Refresh.refresh_unit_graphics_list(play_obj, qrs)



    @staticmethod
    def change_hex_colour_handler(play_obj, flag, site, stage):
        
        if stage == 0 and site == 'C':
            matching = gamelogic.GameLogic.get_matching_coords(play_obj.game.board.hexes, gamelogic.GameLogic.deploy0_right_hex_S)
        elif stage == 0 and site == 'Z':
            matching = gamelogic.GameLogic.get_matching_coords(play_obj.game.board.hexes, gamelogic.GameLogic.deploy0_right_hex_W)
        else:
            return

        PlayHandler.change_hex_colour(play_obj, flag, matching)
    
   
      
       
       