import control_obj
import kolor
import pygame
import hexagon
import camera
import play_handler
import gamelogic
from functools import partial # Powoduje, że funkcja x() jest wywoływana bez argumentów

class Play(object):

    def __init__(self, screen, gameController, connection, game):

        self.screen = screen
        self.gameController = gameController
        self.connection = connection
        self.game = game
        self.camera = camera.Camera()
        self.hex_size = screen.get_height() * 0.024
        self.stageFields = []
        self.phazeFields = []
        self.units = []
        self.reinforcement = []

        self.playerWfield = control_obj.Label(0, 0, screen.get_width() * 0.1, screen.get_height() // 2,
            kolor.GREEN, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.playerWlogin = control_obj.Label(3, 3, int(self.playerWfield.getWidth()  - 6), 
            int(self.playerWfield.getHeight() * 0.06), kolor.WHITE, self.game.playerW.getLogin(), 
            self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, 
            None, None, None, None)
        self.playerWphoto = control_obj.Label(3, self.playerWlogin.getHeight() + 6, 
            int((self.playerWfield.getWidth()  - 9) / 2), int((self.playerWfield.getWidth()  - 9) / 2),
            kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.playerWdemoralization1 = control_obj.Label(self.playerWphoto.getWidth() + 6, 
            self.playerWlogin.getHeight() + 6, int((self.playerWphoto.getWidth() - 3) / 2), 
            int((self.playerWphoto.getHeight() - 3) / 2), kolor.WHITE, 
            str(self.game.playerW.getDemoralizationTreshold2()), self.gameController.getDefaultFont(), 
            int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerWdemoralization2 = control_obj.Label(self.playerWphoto.getWidth() + 9 + 
            self.playerWdemoralization1.getWidth(), self.playerWlogin.getHeight() + 6, 
            int((self.playerWphoto.getWidth() - 3) / 2), int((self.playerWphoto.getHeight() - 3) / 2), 
            kolor.WHITE, str(self.game.playerW.getDemoralizationTreshold3()), self.gameController.getDefaultFont(), 
            int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerWspellPower = control_obj.Label(self.playerWphoto.getWidth() + 6, 
            self.playerWlogin.getHeight() + self.playerWdemoralization1.getHeight() + 9, 
            int((self.playerWphoto.getWidth() - 3) / 2), int((self.playerWphoto.getHeight() - 3) / 2), kolor.WHITE, 
            str(self.game.playerW.getSpellPower()), self.gameController.getDefaultFont(), 
            int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None) 
        self.playerSfield = control_obj.Label(0, self.playerWfield.getHeight(), screen.get_width() * 0.1, 
            screen.get_height() // 2, kolor.RED, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.playerSlogin = control_obj.Label(3, self.playerSfield.getHeight() + 3, 
            int(self.playerSfield.getWidth()  - 6), int(self.playerSfield.getHeight() * 0.06), kolor.WHITE, 
            self.game.playerS.getLogin(), self.gameController.getDefaultFont(), 
            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerSphoto = control_obj.Label(3, self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight(), 
            int((self.playerSfield.getWidth()  - 9) / 2), int((self.playerSfield.getWidth()  - 9) / 2),
            kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.playerSdemoralization = control_obj.Label(self.playerSphoto.getWidth() + 6, 
            self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight() , int((self.playerSphoto.getHeight() - 3) / 2), 
            int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, 
            str(self.game.playerS.getDemoralizationTreshold1()), self.gameController.getDefaultFont(), 
            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerSspellPower = control_obj.Label(self.playerSphoto.getWidth() + 6, 
            self.playerSlogin.getHeight() + self.playerSdemoralization.getHeight() + 9 + self.playerSfield.getHeight(), 
            int((self.playerSphoto.getWidth() - 3) / 2), int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, 
            str(self.game.playerS.getSpellPower()), self.gameController.getDefaultFont(), 
            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerSHeads = control_obj.Label(self.playerSphoto.getWidth() + 9 + 
            self.playerSspellPower.getWidth(), self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight(), 
            int((self.playerSphoto.getWidth() - 3) / 2), int((self.playerSphoto.getHeight() - 3) / 2), 
            kolor.WHITE, str(self.game.playerS.getHeads()), self.gameController.getDefaultFont(), 
            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.stateField = control_obj.Label(screen.get_width() - screen.get_width() * 0.1, 0, screen.get_width() * 0.101, screen.get_height(),
            kolor.BLUE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, None, None, None, None)
        self.map = control_obj.Label(screen.get_width() * 0.1, 0, screen.get_width() + screen.get_width() * 0.366, 
            screen.get_height() + screen.get_height() * 0.462, kolor.ORANGE, "", None, int(screen.get_height() * 0.035), kolor.WHITE, 
            None, None, partial(play_handler.ZoomOutHandler.handle, self.getCamera()), 
            partial(play_handler.ZoomInHandler.handle, self.getCamera()))
        self.zoomInButton = control_obj.Button(self.stateField.getPositionX() + (screen.get_height() * 0.0028), 
            screen.get_height() * 0.0028, screen.get_height() * 0.028, screen.get_height() * 0.028, kolor.GREY, "+", 
            self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, 
            partial(play_handler.ZoomInHandler.handle, self.getCamera()), None, None, None)
        self.zoomOutButton = control_obj.Button(self.stateField.getPositionX() + (screen.get_height() * 0.033),
            screen.get_height() * 0.0028, screen.get_height() * 0.028, screen.get_height() * 0.028, kolor.GREY, "-", 
            self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, 
            partial(play_handler.ZoomOutHandler.handle, self.getCamera()), None, None, None)
        self.diceButton = control_obj.Button(
            self.stateField.getPositionX() + (self.stateField.getWidth() // 3 // 3), len(self.game.getStagesList())
            * (self.stateField.getHeight() / 24) + screen.get_height() * 0.033 + screen.get_height() * 0.028 + 26,
            self.stateField.getWidth() // 3, self.stateField.getWidth() // 3, kolor.GREY, "", 
            self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, 
            None, None, None, None)
        self.resultField = control_obj.Label(
            self.diceButton.getPositionX() + self.diceButton.getWidth() + (self.stateField.getWidth() // 3 // 3), 
            self.diceButton.getPositionY(),self.stateField.getWidth() // 3, self.stateField.getWidth() // 3, 
            kolor.WHITE,  "",  self.gameController.getDefaultFont(), int(screen.get_height() * 0.03), kolor.BLACK, 
            None, None, None, None)
        self.messageField = control_obj.Label(
            self.stateField.getPositionX() + (screen.get_height() * 0.0028),  self.diceButton.getPositionY() + 
            self.diceButton.getHeight() + 10,  self.stateField.getWidth() - (screen.get_height() * 0.0028 * 2), 
            screen.get_height() * 0.100, kolor.WHITE, "", self.gameController.getDefaultFont(), int(screen.get_height() * 0.025), 
            kolor.BLACK, None, None, None, None)
        self.actionButton = control_obj.Button(
            self.stateField.getPositionX() + (screen.get_height() * 0.0028), self.messageField.getPositionY() + 
            self.messageField.getHeight() + 3, self.stateField.getWidth() - (screen.get_height() * 0.0028 * 2), 
            screen.get_height() * 0.045, kolor.GREY, "", self.gameController.getDefaultFont(), int(screen.get_height() * 0.03),
            kolor.BLACK, None, None, None, None)
        
        self.hex_surface = None
        self._last_camera_state = (None, None, None)
        self._initStageAndPhazeFields()
        self._board_changed = True


    def checkReinforcement(self):
        if self.gameController.getDeploy():
            self.addReinforcement()


    def addReinforcement(self):
        unitW = self.game.getPlayerWUnits()
        unitS = self.game.getPlayerSUnits()
        width = (self.playerWfield.getWidth() - 15) // 4
        height = width
        margin = 3 
        quantityInRow = int(self.playerWfield.getWidth() // (width + margin))

        inRow = 0
        column = 0
      
        for unit in unitW:
            if unit.getStageDeploy() <= self.gameController.getAktStage():
                if inRow <= quantityInRow:
                    positionX = self.playerWfield.getPositionX() + 3 + (width + margin) * inRow
                    positionY = self.playerWphoto.getPositionY() + self.playerWphoto.getHeight() + 3 + (height + margin) * column
                    unitG = control_obj.UnitGraph(
                        positionX, positionY, width, height, kolor.LIME, gamelogic.GameLogic.unitFullString(unit, self.gameController.getChoosedSite()), self.gameController.getDefaultFont(), int(height * 0.94 / 3), kolor.BLACK, None, None, None, None, unit)
                    self.reinforcement.append(unitG)
                    inRow += 1
                    if inRow == quantityInRow:
                        inRow = 0
                        column += 1

        inRow = 0
        column = 0
      
        for unit in unitS:
            if unit.getStageDeploy() <= self.gameController.getAktStage():
                if inRow <= quantityInRow:
                    positionX = self.playerWfield.getPositionX() + 3 + (width + margin) * inRow
                    positionY = self.playerSphoto.getPositionY() + self.playerSphoto.getHeight() + 3 + (height + margin) * column
                    unitG = control_obj.UnitGraph(
                        positionX, positionY, width, height, kolor.REDJ, gamelogic.GameLogic.unitFullString(unit, self.gameController.getChoosedSite()), self.gameController.getDefaultFont(), int(height * 0.94 / 3), kolor.BLACK, None, None, None, None, unit)
                    self.reinforcement.append(unitG)
                    inRow += 1
                    if inRow == quantityInRow:
                        inRow = 0
                        column += 1

        self.gameController.setDeploy(False)         


    def _setMaxCamera(self, screenwidth, screenheight):
        self.camera.setCameraX(max(0, min(self.camera.getCameraX(), self.map.getWidth() - screenwidth)))
        self.camera.setCameraY(max(0, min(self.camera.getCameraY(), self.map.getHeight() - screenheight)))


    def _initStageAndPhazeFields(self):
        stages = self.game.getStagesList()
        phazes = self.game.getPhazesList()
        width = self.stateField.getWidth()
        height = self.stateField.getHeight()
        conStageHeight = int(height / 24)
        stageheight = int(height / 24)
        phazewidth = (width - 6) // 9
        phazeheight = conStageHeight * 0.96 // 2

        self.stageFields.clear()
        self.phazeFields.clear()

        for stage in stages:
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
                stage.getSeason(),
                stage.getText()
            )
            self.stageFields.append(stageField)
            stageheight += conStageHeight + 2

        stageheight = int(height / 24)
        i = 0
        for phaze in phazes:
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
                phaze.getNrStage(),
                phaze.getName()
            )
            self.phazeFields.append(phazeField)
            if i % 8 == 0:
                i = 0
                stageheight += conStageHeight + 2


    def getCamera(self):
        return self.camera


    def getHexSize(self):
        return self.hex_size


    def drawPlay(self, screen, mousePosition):
        self.playerWfield.draw(screen)
        self.playerSfield.draw(screen)
        self.playerWlogin.draw(screen)
        self.playerWphoto.draw(screen)
        self.playerWdemoralization1.draw(screen)
        self.playerWdemoralization2.draw(screen)
        self.playerWspellPower.draw(screen)
        self.playerSlogin.draw(screen)
        self.playerSphoto.draw(screen)
        self.playerSdemoralization.draw(screen)
        self.playerSspellPower.draw(screen)
        self.playerSHeads.draw(screen)
        self.map.draw(screen)
        self.drawHexes(screen)
        self.stateField.draw(screen)
        self.drawZoomButtons(screen, mousePosition)
        self.drawStagePhaze(screen, mousePosition)
        self.diceButton.draw(screen)
        self.resultField.draw(screen)
        self.messageField.draw(screen)
        self.actionButton.draw(screen)
        self.checkReinforcement()
        self.drawUnits(screen, mousePosition)


    def drawUnits(self, screen, mousePosition):    
        for reinforcement in self.reinforcement:
            reinforcement.draw(screen)
            if reinforcement.isOverObject(mousePosition):
                screen_width = screen.get_width()
                screen_height = screen.get_height()
                max_line_width = screen_width * 0.08
                site = self.gameController.getChoosedSite()
                name = gamelogic.GameLogic.changePotName(reinforcement.unit, site)
                text = f"{name}\n {reinforcement.unit.nationality}\n {reinforcement.text[2]}"
                control_obj.Description.draw(screen, text, max_line_width, (self.playerWfield.getWidth() - max_line_width) // 2, mousePosition[1] - 85, self.gameController.getDefaultFont(), int(screen_height * 0.015))
                if reinforcement.unit.getSite() == 'Z':
                    reinforcement.setColour(kolor.RLIME)
                elif reinforcement.unit.getSite() == 'C':
                    reinforcement.setColour(kolor.RREDJ)
            else:
                if reinforcement.unit.getSite() == 'Z':
                    reinforcement.setColour(kolor.LIME)
                elif reinforcement.unit.getSite() == 'C':
                    reinforcement.setColour(kolor.REDJ)
               


    def drawHexes(self, screen):
        current_camera_state = (
            self.camera.getCameraX(),
            self.camera.getCameraY(),
            self.camera.getCameraScale()
        )

        if self.hex_surface is None or current_camera_state != self._last_camera_state or self._board_changed:
            self._last_camera_state = current_camera_state
            self._board_changed = False

            self.hex_surface = pygame.Surface((self.map.getWidth(), self.map.getHeight()))
            self.hex_surface.fill(kolor.ORANGE)

            hexagon.Hexagon.draw_map(
                self.hex_surface,
                self.getHexSize() * self.camera.getCameraScale(),
                -self.camera.getCameraX() * self.camera.getCameraScale(),
                -self.camera.getCameraY() * self.camera.getCameraScale(),
                self.game.board.getHexes()
            )

        screen.blit(self.hex_surface, (self.map.getPositionX(), self.map.getPositionY()))



    def invalidateHexSurface(self):
        self.hex_surface = None


    def notifyBoardChanged(self):
        self._board_changed = True


    def drawStagePhaze(self, screen, mousePosition):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        max_line_width = screen_width * 0.1
        positionX = screen_width - self.stateField.getWidth() - max_line_width - 10
        positionY = mousePosition[1] - 10

        for stageField in self.stageFields:
            stageField.draw(screen)

        for phazeField in self.phazeFields:
            phazeField.draw(screen)

        for phaze, phazeField in zip(self.game.getPhazesList(), self.phazeFields):
            if phazeField.isOverObject(mousePosition):  
                text = f"Faza {phaze.getNrPhaze()}: {phaze.getName()}"
                control_obj.Description.draw(screen, text, max_line_width, positionX, positionY, 
                            self.gameController.getDefaultFont(), int(screen_height * 0.015))
                return

        for stage, stageField in zip(self.game.getStagesList(), self.stageFields):
            if stageField.isOverObject(mousePosition):
                text = f"ETAP {stage.getNrStage()}: {stage.getSeason()} \n {stage.getText()}"
                control_obj.Description.draw(screen, text, max_line_width, positionX, positionY, 
                            self.gameController.getDefaultFont(), int(screen_height * 0.015))
                return

    def drawZoomButtons(self, screen, mousePosition):
        if self.zoomInButton.isOverObject(mousePosition):
            self.zoomInButton.setColour(kolor.RGREY)
        else:
            self.zoomInButton.setColour(kolor.GREY)

        if self.zoomOutButton.isOverObject(mousePosition):
            self.zoomOutButton.setColour(kolor.RGREY)
        else:
            self.zoomOutButton.setColour(kolor.GREY)
        self.zoomInButton.draw(screen)
        self.zoomOutButton.draw(screen)


    def handleEvent(self, mousePosition, event):
        self.zoomInButton.handle_event(mousePosition, event)
        self.zoomOutButton.handle_event(mousePosition, event)
        self.map.handle_event(mousePosition, event)


    def handleKeyboardEvent(self, event):
        if event.key == pygame.K_ESCAPE:
            self.connection.close_connection()
            pygame.quit()
            quit()


    def updateMovement(self, screen, keys):
        if keys[pygame.K_LEFT]:
            self.camera.setCameraX(self.camera.getCameraX() - self.camera.getCameraSpeed())
        if keys[pygame.K_RIGHT]:
            self.camera.setCameraX(self.camera.getCameraX() + self.camera.getCameraSpeed())
        if keys[pygame.K_UP]:
            self.camera.setCameraY(self.camera.getCameraY() - self.camera.getCameraSpeed())
        if keys[pygame.K_DOWN]:
            self.camera.setCameraY(self.camera.getCameraY() + self.camera.getCameraSpeed())

        self._setMaxCamera(screen.get_width(), screen.get_height())

    
