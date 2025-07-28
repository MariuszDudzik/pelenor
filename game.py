import player
import board
import stage
import phaze
import gamelogic

class Game(object):

    def __init__(self):
        self.player_w = player.Player('', 'Z', '', 0, None)
        self.player_s = player.Player('', 'C', '', 0, None)
        self.board = board.Board()
        self.minas_tirith_dict = None
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
    
    def get_player_w(self):
        return self.player_w
    
    def get_player_s(self):
        return self.player_s
    
    def set_minas_tirith_dict(self):
        self.minas_tirith_dict = gamelogic.GameLogic.create_mn_level_dict(self.board.get_hexes())
    
    

    
      

        