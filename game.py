import player
import board

class Game(object):

    def __init__(self):
        self.playerW = player.Player('', 'Z', '', 0, None)
        self.playerS = player.Player('', 'C', '', 0, None)
        self.board = board.Board()
      

        