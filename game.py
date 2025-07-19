import player
import board
import stage
import phaze

class Game(object):

    def __init__(self):
        self.player_w = player.Player('', 'Z', '', 0, None)
        self.player_s = player.Player('', 'C', '', 0, None)
        self.board = board.Board()
        self.stages = stage.create_stage()
        self.phazes = phaze.create_phaze()

    def get_stages_list(self):
        return self.stages

    def get_phazes_list(self):
        return self.phazes

    def get_player_site(self, login):
        if login == self.player_w.get_login():
            return 'W'
        elif login == self.player_s.get_login():
            return 'S'

    def get_player_w_units(self):
        return self.player_w.get_units()

    def get_player_s_units(self):
        return self.player_s.get_units()

    def get_board(self):
        return self.board
    

    
      

        