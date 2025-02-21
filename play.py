import control_obj
import kolor

class Play(object):

    def __init__(self, screenWidth, screenHeight, gameController, connection):

        self.gameController = gameController
        self.connection = connection

        self.playerWfield = control_obj.Label(0, 0, screenWidth * 0.1, screenHeight // 2,
            kolor.GREEN, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        self.playerSfield = control_obj.Label(0, self.playerWfield.getHeight(), screenWidth * 0.1, 
            screenHeight // 2, kolor.RED, "", None, int(screenHeight * 0.035), kolor.WHITE, None, 
            None, None, None)
        self.stateField = control_obj.Label(screenWidth - screenWidth * 0.1, 0, screenWidth * 0.101, screenHeight,
            kolor.BLUE, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        self.map = control_obj.Label(screenWidth * 0.1, 0, screenWidth + screenWidth * 0.366, screenHeight +          screenHeight * 0.462, kolor.ORANGE, "", None, int(screenHeight * 0.035), kolor.WHITE, None, None, None, None)
        


    def drawPlay(self, screen):
        self.playerWfield.draw(screen)
        self.playerSfield.draw(screen)
        self.map.draw(screen)
        self.stateField.draw(screen)
        
