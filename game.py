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
      

        