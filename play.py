import control_obj
import kolor
import pygame
import hexagon
import camera
import play_handler
import gamelogic
import hexagon
from functools import partial # Powoduje, że funkcja x() jest wywoływana bez argumentów

class Play(object):

    def __init__(self, screen, gameController, connection, game):

        self.screen = screen
        self.gameController = gameController
        self.connection = connection
        self.game = game
        self.camera = camera.Camera()
        self.hex_size = screen.get_height() * (0.017 + self.camera.getCameraScale() * self.camera.getZoomSpeed())
        self.stageFields = []
        self.phazeFields = []
        self.hex = {}
        self.units = {}
        self.reinforcement = {}
        self.leftMenuGraphics = pygame.sprite.LayeredDirty()
        self.rightMenuGraphics = pygame.sprite.LayeredDirty()
        self.mapView = pygame.sprite.LayeredDirty()
        self.manageGraphics = pygame.sprite.LayeredDirty()
        self.stagePhazeGraphics = pygame.sprite.LayeredDirty()
        self.toolTipGraphics = pygame.sprite.LayeredDirty()
        self.mouse_dragging = False
        self.last_mouse_pos = None 

        self.playerWfield = control_obj.Label(0, 0, screen.get_width() * 0.1, screen.get_height() // 2,
                            kolor.GREEN, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.playerWlogin = control_obj.Label(3, 3, int(self.playerWfield.getWidth()  - 6), 
                            int(self.playerWfield.getHeight() * 0.06), kolor.WHITE, self.game.playerW.getLogin(), 
                            self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.playerWphoto = control_obj.Label(3, self.playerWlogin.getHeight() + 6, int((self.playerWfield.getWidth() 
                            - 9) / 2), int((self.playerWfield.getWidth()  - 9) / 2), kolor.BLUE, "", None, 
                            int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.playerWdemoralization1 = control_obj.Label(self.playerWphoto.getWidth() + 6, self.playerWlogin.getHeight() 
                            + 6, int((self.playerWphoto.getWidth() - 3) / 2), int((self.playerWphoto.getHeight() - 3) / 2), kolor.WHITE, str(self.game.playerW.getDemoralizationTreshold2()), 
                            self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8),
                            kolor.BLACK, None, None, None, None, None, None)
        self.playerWdemoralization2 = control_obj.Label(self.playerWphoto.getWidth() + 9 
                            + self.playerWdemoralization1.   getWidth(), self.playerWlogin.getHeight() + 6, 
                            int((self.playerWphoto.getWidth() - 3) / 2), int((self.playerWphoto.getHeight() - 3) / 2), 
                            kolor.WHITE, str(self.game.playerW.getDemoralizationTreshold3()), 
                            self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.playerWspellPower = control_obj.Label(self.playerWphoto.getWidth() + 6, self.playerWlogin.getHeight() 
                            + self.playerWdemoralization1.getHeight() + 9, int((self.playerWphoto.getWidth() - 3) / 2), int((self.playerWphoto.getHeight() - 3) / 2), kolor.WHITE, 
                            str(self.game.playerW.getSpellPower()), self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None) 
        self.playerSfield = control_obj.Label(0, self.playerWfield.getHeight(), screen.get_width() * 0.1, 
                            screen.get_height() // 2, kolor.RED, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.playerSlogin = control_obj.Label(3, self.playerSfield.getHeight() + 3, int(self.playerSfield.getWidth() 
                            - 6), int(self.playerSfield.getHeight() * 0.06), kolor.WHITE, self.game.playerS.getLogin(), self.gameController.getDefaultFont(), int(self.playerSfield.getHeight() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.playerSphoto = control_obj.Label(3, self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight(), 
                            int((self.playerSfield.getWidth()  - 9) / 2), int((self.playerSfield.getWidth()  - 9) / 2),
                            kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.playerSdemoralization = control_obj.Label(self.playerSphoto.getWidth() + 6, 
                            self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight() , 
                            int((self.playerSphoto.getHeight() - 3) / 2), int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, str(self.game.playerS.getDemoralizationTreshold1()), 
                            self.gameController.getDefaultFont(), int(self.playerSfield.getHeight() * 0.06 * 0.8), 
                            kolor.BLACK, None, None, None, None, None, None)
        self.playerSspellPower = control_obj.Label(self.playerSphoto.getWidth() + 6, 
                            self.playerSlogin.getHeight() + self.playerSdemoralization.getHeight() + 9 + 
                            self.playerSfield.getHeight(), int((self.playerSphoto.getWidth() - 3) / 2), 
                            int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, 
                            str(self.game.playerS.getSpellPower()), self.gameController.getDefaultFont(), 
                            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None)
        self.playerSHeads = control_obj.Label(self.playerSphoto.getWidth() + 9 + self.playerSspellPower.getWidth(), 
                            self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight(), int((self.playerSphoto.getWidth() - 3) / 2), int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, 
                            str(self.game.playerS.getHeads()), self.gameController.getDefaultFont(), int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None, None, None)
        self.stateField = control_obj.Label(screen.get_width() - screen.get_width() * 0.1, 0, screen.get_width() * 0.101 
                            ,screen.get_height(), kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None, None, None)
        self.map = control_obj.Label(self.playerWfield.getWidth(), 0, self.screen.get_width() - 
                            self.playerWfield.getWidth() - self.stateField.getWidth(), self.screen.get_height(), 
                            kolor.ORANGE, "", None,  int(screen.get_height() * 0.035), kolor.WHITE, None, None,
                            partial(play_handler.ZoomHandler.handleIn, self.getCamera, self), 
                            partial(play_handler.ZoomHandler.handleOut, self.getCamera, self), None, None)
        self.zoomInButton = control_obj.Button(self.stateField.getPositionX() + (screen.get_height() * 0.0028), 
                            screen.get_height() * 0.0028, screen.get_height() * 0.028, screen.get_height() * 0.028, 
                            kolor.GREY, "+", self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, partial(play_handler.ZoomHandler.handleIn, self.getCamera, self), None, None, None, play_handler.ZoomHandler.onHover, play_handler.ZoomHandler.unHover)
        self.zoomOutButton = control_obj.Button(self.stateField.getPositionX() + (screen.get_height() * 0.033),
                            screen.get_height() * 0.0028, screen.get_height() * 0.028, screen.get_height() * 0.028, 
                            kolor.GREY, "-", self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, partial(play_handler.ZoomHandler.handleOut, self.getCamera, self), None, None, None, play_handler.ZoomHandler.onHover, play_handler.ZoomHandler.unHover)
        self.diceButton = control_obj.Button(self.stateField.getPositionX() + (self.stateField.getWidth() // 3 // 3),
                            len(self.game.getStagesList()) * (self.stateField.getHeight() / 24) + screen.get_height() * 0.033 + screen.get_height() * 0.028 + 26, self.stateField.getWidth() // 3, self.stateField.getWidth() // 3, kolor.GREY, "", self.gameController.getDefaultFont(), 
                            int(screen.get_height() * 0.03), kolor.BLACK, None, None, None, None, None, None)
        self.resultField = control_obj.Label(self.diceButton.getPositionX() + self.diceButton.getWidth() 
                            + (self.stateField.getWidth() // 3 // 3), self.diceButton.getPositionY(),self.stateField.getWidth() // 3, self.stateField.getWidth() // 3, kolor.WHITE,  "",  self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, None, None, None, None, None, None)
        self.messageField = control_obj.Label(self.stateField.getPositionX() + (screen.get_height() * 0.0028),  
                            self.diceButton.getPositionY() + self.diceButton.getHeight() + 10,  self.stateField.getWidth() - (screen.get_height() * 0.0028 * 2), screen.get_height() * 0.100, kolor.WHITE, "", self.gameController.getDefaultFont(), int(screen.get_height() * 0.025), kolor.BLACK, None, None, None, None, None, None)
        self.actionButton = control_obj.Button(self.stateField.getPositionX() + (screen.get_height() * 0.0028), 
                            self.messageField.getPositionY() + self.messageField.getHeight() + 3, self.stateField.getWidth() - (screen.get_height() * 0.0028 * 2), screen.get_height() * 0.045, kolor.GREY, "", self.gameController.getDefaultFont(), int(screen.get_height() * 0.03),kolor.BLACK, None, None, None, None, None, None)
        self.toolTip = control_obj.Tooltip(0, 0, 0, 0, kolor.WHITE, "", self.gameController.getDefaultFont()
                            , int(screen.get_height() * 0.015), kolor.BLACK, None, None, None, None, None, None)
        
        self._initStageAndPhazeFields()
        self._prepareGraphics()
        self.setMapView()
        self.camera.setMinX(-0.066 * self.screen.get_height() * 44)
        self.camera.setMinY(-0.066 * self.screen.get_height() * 31)
        self.toolTip.dirty = 0
        

    def setHexBaseSize(self):
        self.hex_size = self.screen.get_height() * (0.017 + self.camera.getCameraScale() * self.camera.getZoomSpeed())


    def setMapView(self):
        self.mapView.empty()
        self.mapView.add(self.map, layer=1)
        visible_hexes = self.get_visible_hexagons(self.getMap(), self.getCamera(), self.getHexSize(), self.game.getBoard().getHexes())
        self.hex = hexagon.Hexagon.create_hex_graphics_dict(self.hex_size, self.getCamera(),
                            visible_hexes, self.getMap())
        self.mapView.add(*self.hex.values(), layer=3)
        for unit in self.game.playerW.getUnits().values():
            if unit.getQRS() is not None:
                self.addUnit('Z', unit.id, unit.getQRS())
        for unit in self.game.playerS.getUnits().values():
            if unit.getQRS() is not None:
                self.addUnit('C', unit.id, unit.getQRS())
        

    def _prepareGraphics(self):
        for sprite in [self.playerWfield, self.playerSfield]:
            self.leftMenuGraphics.add(sprite, layer=1)
        for sprite in [self.playerWlogin,self.playerWphoto, self.playerWdemoralization1, self.playerWdemoralization2,
                    self.playerWspellPower, self.playerSlogin, self.playerSphoto,self.playerSdemoralization, self.playerSspellPower, self.playerSHeads]:
            self.leftMenuGraphics.add(sprite, layer=2)
        self.rightMenuGraphics.add(self.stateField, layer=1)
        self.manageGraphics.add(self.zoomInButton, self.zoomOutButton, self.diceButton, self.resultField,
                                self.messageField, self.actionButton, layer=4)
        for sprite in self.stageFields:
            self.stagePhazeGraphics.add(sprite, layer=2)
        for sprite in self.phazeFields:
            self.stagePhazeGraphics.add(sprite, layer=3)
        self.toolTipGraphics.add(self.toolTip, layer=5)


    def addReinforcementGraphics(self):
        self.leftMenuGraphics.add(*self.reinforcement.values(), layer=4)

  
    def _initStageAndPhazeFields(self):
        stages = self.game.getStagesList()
        phazes = self.game.getPhazesList()
        width = self.stateField.getWidth()
        height = self.stateField.getHeight()
        conStageHeight = int(height / 24)
        stageheight = int(height / 24)
        phazewidth = (width - 6) // 9
        phazeheight = conStageHeight * 0.96 // 2
        maxlinewidth = self.screen.get_width() * 0.1
        tooltipX = self.screen.get_width() - self.stateField.getWidth() - maxlinewidth - 10
       
        self.stageFields.clear()
        self.phazeFields.clear()

        for stage in stages:
            text =  f"ETAP {stage.getNrStage()}: {stage.getSeason()} \n {stage.getText()}"
            stageField = control_obj.StageGraph(
                self.stateField.getPositionX() + 3,
                stageheight,
                width - 6,
                conStageHeight,
                stage.getColour(),
                "",
                None,
                int(height * 0.035),
                kolor.WHITE,
                None,
                None,
                None,
                None,
                partial(play_handler.ToolTipHandler.onHover, get_toolTip=self.getToolTip, toolX=tooltipX, toolY=stageheight, max_line_width=maxlinewidth),
                partial(play_handler.ToolTipHandler.unHover, play_obj=self),
                stage,

            )
            stageField.tiptext = text
            self.stageFields.append(stageField)
            stageheight += conStageHeight + 2

        stageheight = int(height / 24)
        i = 0
        for phaze in phazes:
            text = f"Faza {phaze.getNrPhaze()}: {phaze.getName()}"
            i += 1
            phazeField = control_obj.PhazeGraph(
                4.8 + self.stateField.getPositionX() + (phazewidth + 2.0) * (i - 1),
                stageheight + conStageHeight * 0.08,
                phazewidth,
                phazeheight,
                phaze.getColour(),
                "",
                None,
                int(height * 0.035),
                kolor.BLACK,
                None,
                None,
                None,
                None,
                partial(play_handler.ToolTipHandler.onHover, get_toolTip=self.getToolTip, toolX=tooltipX, toolY=stageheight, max_line_width=maxlinewidth),
                partial(play_handler.ToolTipHandler.unHover, play_obj=self),
                phaze,
            )
            phazeField.tiptext = text
            self.phazeFields.append(phazeField)
            if i % 8 == 0:
                i = 0
                stageheight += conStageHeight + 2


    """
    def checkReinforcement(self):
        if self.gameController.getDeploy():
            self.addReinforcement()
    """

    def addUnit(self, site, id, qrs):
        qrs = tuple(qrs)
        if qrs in self.hex:
            if site == 'C':
                units = self.game.getPlayerSUnits()
                colour = kolor.REDJ
                self.game.getPlayerSUnits()[id].setDeploy()
                self.game.getPlayerSUnits()[id].setQRS(qrs)
            elif site == 'Z':
                units = self.game.getPlayerWUnits()
                colour = kolor.LIME
                self.game.getPlayerWUnits()[id].setDeploy()
                self.game.getPlayerWUnits()[id].setQRS(qrs)
            size = self.hex[qrs].getCurrentSize() * 1.3 
            pos_x = self.hex[qrs].getCurrentCenter()[0] - size / 2
            pos_y = self.hex[qrs].getCurrentCenter()[1] - size / 2
            

            unitG = control_obj.UnitGraph(
                            pos_x, pos_y, size, size, colour,"",self.gameController.getDefaultFont(),
                            int(size * 0.85 / 3), kolor.BLACK, None, None, None, None, None, None, self.getMap(), 
                            unit = units[id])
            unitG.wrapped_lines = gamelogic.GameLogic.unitFullString(units[id], self.gameController.getChoosedSite())
            text = f"{units[id].name}\n {units[id].nationality}\n {unitG.wrapped_lines[2]}"
            unitG.setTipText(text)
            self.units[id] = unitG

            i = len(self.game.getBoard().getHexes()[qrs].pawnList)
            self.game.getBoard().getHexes()[qrs].pawnList.append(id)
            self.mapView.add(unitG, layer=10 + i)


    def addReinforcement(self):
        maxlinewidth = self.screen.get_width() * 0.08
        tooltipX = self.playerWfield.getPositionX() + 5
        unitW = self.game.getPlayerWUnits()
        unitS = self.game.getPlayerSUnits()

        width = (self.playerWfield.getWidth() - 15) // 4
        height = width
        margin = 3 
        quantityInRow = int(self.playerWfield.getWidth() // (width + margin))

        self.reinforcement = {}

        inRow = 0
        column = 0
    
        for unit in unitW.values():
            if unit.getStageDeploy() <= self.gameController.getAktStage() and unit.getDeploy() == False:
                if inRow <= quantityInRow:
                    
                    positionX = self.playerWfield.getPositionX() + 3 + (width + margin) * inRow
                    positionY = self.playerWphoto.getPositionY() + self.playerWphoto.getHeight() + 3 + (height + margin) * column
                    unitG = control_obj.UnitGraph(
                        positionX, positionY, width, height, kolor.LIME,"",self.gameController.getDefaultFont(),
                        int(height * 0.85 / 3), kolor.BLACK, None, None, None, None, 
                        partial(play_handler.ToolTipHandler.onHoverReinforcement, get_toolTip=self.getToolTip, toolX=tooltipX, toolY=positionY - 75, max_line_width=maxlinewidth), 
                        partial(play_handler.ToolTipHandler.unHoverReinforcement, play_obj=self), None, unit)
                    unitG.wrapped_lines = gamelogic.GameLogic.unitFullString(unit, self.gameController.getChoosedSite())

                    text = f"{gamelogic.GameLogic.changePotName(unit, self.gameController.getSite())}\n {unit.nationality}\n {unitG.wrapped_lines[2]}"
                    unitG.setTipText(text)
                    self.reinforcement[unit.id] = unitG
                    inRow += 1
                    if inRow == quantityInRow:
                        inRow = 0
                        column += 1

        inRow = 0
        column = 0
    
        for unit in unitS.values():
            if unit.getStageDeploy() <= self.gameController.getAktStage() and unit.getDeploy() == False:
                if inRow <= quantityInRow:
                    positionX = self.playerWfield.getPositionX() + 3 + (width + margin) * inRow
                    positionY = self.playerSphoto.getPositionY() + self.playerSphoto.getHeight() + 3 + (height + margin) * column
                    unitG = control_obj.UnitGraph(
                        positionX, positionY, width, height, kolor.REDJ,"", self.gameController.getDefaultFont(),
                        int(height * 0.85 / 3), kolor.BLACK, None, None, None, None,
                        partial(play_handler.ToolTipHandler.onHoverReinforcement, get_toolTip=self.getToolTip, toolX=tooltipX, toolY=positionY - 85, max_line_width=maxlinewidth), 
                        partial(play_handler.ToolTipHandler.unHoverReinforcement, play_obj=self), None, unit)
                    unitG.wrapped_lines = gamelogic.GameLogic.unitFullString(unit, self.gameController.getChoosedSite())
                    text = f"{unit.name}\n {unit.nationality}\n {unitG.wrapped_lines[2]}"
                    unitG.setTipText(text)
                    self.reinforcement[unit.id] = unitG
                    inRow += 1
                    if inRow == quantityInRow:
                        inRow = 0
                        column += 1


    def setAllDirty(self):
        for sprite in self.leftMenuGraphics:
            sprite.setDirty()
        for sprite in self.rightMenuGraphics:
            sprite.setDirty()
        for sprite in self.mapView:
            sprite.setDirty()
        for sprite in self.manageGraphics:
            sprite.setDirty()
        for sprite in self.stagePhazeGraphics:
            sprite.setDirty()
        

    def render(self, mousePosition):
        all_dirty_rects = []

        self.mapView.update(mousePosition)
        for sprite in self.mapView:
            if sprite.dirty:
                sprite.draw(self.screen.get_screen())
                all_dirty_rects.append(sprite.rect.copy())
    
        self.leftMenuGraphics.update(mousePosition)
        dirty_rects = self.leftMenuGraphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.rightMenuGraphics.update(mousePosition)
        dirty_rects = self.rightMenuGraphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.manageGraphics.update(mousePosition)
        dirty_rects = self.manageGraphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.stagePhazeGraphics.update(mousePosition)
        dirty_rects = self.stagePhazeGraphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        self.toolTipGraphics.update(mousePosition)
        dirty_rects = self.toolTipGraphics.draw(self.screen.get_screen())
        all_dirty_rects.extend(dirty_rects)

        if all_dirty_rects:
            pygame.display.update(all_dirty_rects)


    def getCamera(self):
        return self.camera

    def getHexSize(self):
        return self.hex_size
    
    def getHexes(self):
        return self.hex
    
    def getMap(self):
        return self.map
    
    def getToolTip(self):
        return self.toolTip


    def get_visible_hexagons(self, map_area, camera, hex_size, hexes):
      
        visible_hexes = {}
        
        left_menu_width = map_area.getPositionX()
        map_y = map_area.getPositionY()
        map_width = map_area.getWidth()
        map_height = map_area.getHeight()
        
        camera_x = camera.getCameraX()
        camera_y = camera.getCameraY()
        
        offset_x = left_menu_width + camera_x
        offset_y = map_y + camera_y
        
        view_left = left_menu_width 
        view_right = left_menu_width + map_width
        view_top = map_y
        view_bottom = map_y + map_height
        
        for pos, hex_obj in hexes.items():
            q, r, s = pos
            
            hex_center = hexagon.Hex(*pos)
            pixel = hexagon.Hexagon.hex_to_pixel(hex_center, hex_size, offset_x, offset_y)
            
            hex_left = pixel.x - hex_size
            hex_right = pixel.x + hex_size
            hex_top = pixel.y - hex_size
            hex_bottom = pixel.y + hex_size
            
            if (hex_right >= view_left and hex_left <= view_right and
                hex_bottom >= view_top and hex_top <= view_bottom):
                
                clip_info = {
                    'clip_left': hex_left < view_left,
                    'clip_right': hex_right > view_right,
                    'clip_top': hex_top < view_top,
                    'clip_bottom': hex_bottom > view_bottom,
                    'fully_visible': (hex_left >= view_left and hex_right <= view_right and
                                    hex_top >= view_top and hex_bottom <= view_bottom)
                }
                
                if not clip_info['fully_visible']:
                    clip_rect = {
                        'left': max(hex_left, view_left),
                        'right': min(hex_right, view_right),
                        'top': max(hex_top, view_top),
                        'bottom': min(hex_bottom, view_bottom)
                    }
                    clip_info['clip_rect'] = clip_rect
                
                visible_hexes[pos] = {
                    'hex_obj': hex_obj,
                    'pixel_pos': pixel,
                    'clip_info': clip_info
                }
        
        return visible_hexes
    
  
    def handleEvent(self, mousePosition, event):
        self.zoomInButton.handle_event(mousePosition, event)
        self.zoomOutButton.handle_event(mousePosition, event)
        self.map.handle_event(mousePosition, event)
        self.toolTip.handle_event(mousePosition, event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_dragging = True
                self.last_mouse_pos = mousePosition
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_dragging = False
                self.last_mouse_pos = None


    def handleMouseMotion(self, mousePosition, event):
        if self.mouse_dragging and self.last_mouse_pos:
            dx = mousePosition[0] - self.last_mouse_pos[0]
            dy = mousePosition[1] - self.last_mouse_pos[1]
            
            sensitivity = 8
            
            if abs(dx) > sensitivity:
                if dx > 0:
                    if self.camera.getCameraX() < self.camera.getMaxX():
                        cam_x = self.camera.getCameraX() + self.camera.getCameraSpeed()
                        self.camera.setCameraX(cam_x)
                        self.setMapView()
                else:
                    if self.camera.getCameraX() > self.camera.getMinX():
                        cam_x = self.camera.getCameraX() - self.camera.getCameraSpeed()
                        self.camera.setCameraX(cam_x)
                        self.setMapView()
                        
            if abs(dy) > sensitivity:
                if dy > 0:
                    if self.camera.getCameraY() < self.camera.getMaxY():
                        cam_y = self.camera.getCameraY() + self.camera.getCameraSpeed()
                        self.camera.setCameraY(cam_y)
                        self.setMapView()
                else:
                    if self.camera.getCameraY() > self.camera.getMinY():
                        cam_y = self.camera.getCameraY() - self.camera.getCameraSpeed()
                        self.camera.setCameraY(cam_y)
                        self.setMapView()
            
            self.last_mouse_pos = mousePosition


    def updateMovement(self, keys):    
        if keys[pygame.K_LEFT]:
            if self.camera.getCameraX() < self.camera.getMaxX():
                cam_x = self.camera.getCameraX() + self.camera.getCameraSpeed()
                self.camera.setCameraX(cam_x)
                self.setMapView()
        if keys[pygame.K_RIGHT]:
            if self.camera.getCameraX() > self.camera.getMinX():
                cam_x = self.camera.getCameraX() - self.camera.getCameraSpeed()
                self.camera.setCameraX(cam_x)
                self.setMapView()
        if keys[pygame.K_UP]:
            if self.camera.getCameraY() < self.camera.getMaxY():
                cam_y = self.camera.getCameraY() + self.camera.getCameraSpeed()
                self.camera.setCameraY(cam_y)
                self.setMapView()
        if keys[pygame.K_DOWN]:
            if self.camera.getCameraY() > self.camera.getMinY():
                cam_y = self.camera.getCameraY() - self.camera.getCameraSpeed()
                self.camera.setCameraY(cam_y)
                self.setMapView()

     
    def handleKeyboardEvent(self, event):
            if event.key == pygame.K_ESCAPE:
                self.connection.close_connection()
                pygame.quit()
                quit()