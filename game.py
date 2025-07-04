import player
import board
import stage
import phaze

class Game(object):

    def __init__(self):
        self.playerW = player.Player('', 'Z', '', 0, None)
        self.playerS = player.Player('', 'C', '', 0, None)
        self.board = board.Board()
        self.stages = stage.createStage()
        self.phazes = phaze.createPhaze()

    def getStagesList(self):
        return self.stages
    
    def getPhazesList(self):
        return self.phazes
    
    def getPlayerSite(self, login):
        if login == self.playerW.getLogin():
            return 'W'
        elif login == self.playerS.getLogin():
            return 'S'
        
    def getPlayerWUnits(self):
        return self.playerW.getUnits()
    
    def getPlayerSUnits(self):
        return self.playerS.getUnits()
    
    def getBoard(self):
        return self.board
    

    
      

        