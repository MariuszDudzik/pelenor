import control_obj
import kolor
import pygame

class Play(object):

    def __init__(self, screenWidth, screenHeight, gameController, connection, game):

        self.gameController = gameController
        self.connection = connection
        self.game = game

        self.playerWfield = control_obj.Label(0, 0, screenWidth * 0.1, screenHeight // 2,
            kolor.GREEN, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        self.playerWlogin = control_obj.Label(3, 3, int(self.playerWfield.getWidth()  - 6), 
            int(self.playerWfield.getHeight() * 0.06), kolor.WHITE, self.game.playerW.getLogin(), 
            self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, 
            None, None, None, None)
        self.playerWphoto = control_obj.Label(3, self.playerWlogin.getHeight() + 6, 
            int((self.playerWfield.getWidth()  - 9) / 2), int((self.playerWfield.getWidth()  - 9) / 2),
            kolor.BLUE, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
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
            int((self.playerWphoto.getWidth() - 3) / 2), int((self.playerWphoto.getHeight() - 3) / 2), kolor.WHITE, str(self.game.playerW.getSpellPower()), self.gameController.getDefaultFont(), int(self.playerWfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None) 
        self.playerSfield = control_obj.Label(0, self.playerWfield.getHeight(), screenWidth * 0.1, 
            screenHeight // 2, kolor.RED, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        self.playerSlogin = control_obj.Label(3, self.playerSfield.getHeight() + 3, 
            int(self.playerSfield.getWidth()  - 6), int(self.playerSfield.getHeight() * 0.06), kolor.WHITE, 
            self.game.playerS.getLogin(), self.gameController.getDefaultFont(), 
            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerSphoto = control_obj.Label(3, self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight(), 
            int((self.playerSfield.getWidth()  - 9) / 2), int((self.playerSfield.getWidth()  - 9) / 2),
            kolor.BLUE, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        self.playerSdemoralization = control_obj.Label(self.playerSphoto.getWidth() + 6, 
            self.playerSlogin.getHeight() + 6 + self.playerSfield.getHeight() , int(self.playerSphoto.getWidth()), 
            int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, 
            str(self.game.playerS.getDemoralizationTreshold1()), self.gameController.getDefaultFont(), 
            int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None)
        self.playerSspellPower = control_obj.Label(self.playerSphoto.getWidth() + 6, 
            self.playerSlogin.getHeight() + self.playerSdemoralization.getHeight() + 9 + self.playerSfield.getHeight(), int((self.playerSphoto.getWidth() - 3) / 2), int((self.playerSphoto.getHeight() - 3) / 2), kolor.WHITE, str(self.game.playerS.getSpellPower()), self.gameController.getDefaultFont(), int(self.playerSfield.getHeight() * 0.06 * 0.8), kolor.BLACK, None, None, None, None) 
        self.stateField = control_obj.Label(screenWidth - screenWidth * 0.1, 0, screenWidth * 0.101, screenHeight,
            kolor.BLUE, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        self.map = control_obj.Label(screenWidth * 0.1, 0, screenWidth + screenWidth * 0.366, 
            screenHeight + screenHeight * 0.462, kolor.ORANGE, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        


    def drawPlay(self, screen):
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
        self.map.draw(screen)
        self.stateField.draw(screen)
        self.drawStagePhaze(screen)


    def drawStagePhaze(self, screen):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        myouseUponPhaze = False
        max_line_width = screen_width * 0.1
        mousePos = pygame.mouse.get_pos()
        positionX = screen_width - self.stateField.getWidth() - max_line_width - 10
        positionY = mousePos[1] - 10
        stages = self.game.getStagesList()
        phazes = self.game.getPhazesList()
        width = self.stateField.getWidth()
        height = self.stateField.getHeight()
        conStageHeight = int(height / 24)
        stageheight = int(height / 24)
        phazewidth = (width - 6)// 9
        phazeheight = conStageHeight * 0.96 // 2
    
        for stage in stages:
            stageField = control_obj.StageGraph(self.stateField.getPositionX() + 3, stageheight, 
                    width - 6, conStageHeight, stage.getColour(), "", None, int(height * 0.035), 
                    kolor.WHITE, None, None, None, None, stage.getSeason(), stage.getText())
            stageField.draw(screen)
            stageheight += conStageHeight + 2

            if not myouseUponPhaze:
                if stageField.isOverObject(mousePos):
                    
                    text = f"ETAP {stage.getNrStage()}: {stage.getSeason()} \n {stage.getText()}"
                    control_obj.Description.draw(screen, text, max_line_width, positionX, positionY, 
                            self.gameController.getDefaultFont(), int(screen_height * 0.015))    

        stageheight = int(height / 24)
        i = 0
        for phaze in phazes:
            i+=1
            phazeField = control_obj.PhazeGraph(4.8 + self.stateField.getPositionX() + 
                    (phazewidth + 2.0) * (i - 1), stageheight + conStageHeight * 0.08, phazewidth, 
                    phazeheight, phaze.getColour(), "", None, int(height * 0.035), kolor.BLACK, None, 
                    None, None, None, phaze.getNrStage(), phaze.getName())
            phazeField.draw(screen)
            if i % 8 == 0:
                i = 0
                stageheight += conStageHeight + 2

            if phazeField.isOverObject(mousePos):  
                text = f"Faza {phaze.getNrPhaze()}: {phaze.getName()}"
                control_obj.Description.draw(screen, text, max_line_width, positionX, positionY, 
                            self.gameController.getDefaultFont(), int(screen_height * 0.015))  

                myouseUponPhaze = True
