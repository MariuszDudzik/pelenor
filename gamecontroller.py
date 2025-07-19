import platform

class GameController(object):
    def __init__(self):
        self.in_game = True
        self.session_id = None
        self.marked_session_id = None
        self.choosed_site = None
        self.choosed_login = None
        self.open_sessions = []
        self.system = platform.system()
        self.default_font = None
        self.akt_stage = 0
        self.akt_phaze = 0
        self.akt_player = 'C'
        self.deploy = True
        self.move = [[None, None, None], [None]]

        self._set_default_font()


    def _set_default_font(self):
        if self.system == 'Windows':
            self.default_font = 'Arial'
        elif self.system == 'Linux':
            self.default_font = 'Liberation Sans'
        else:
            self.default_font = 'None'

    def get_redraw_sessions(self):
        return self.redraw_sessions

    def set_redraw_sessions(self, redraw):
        self.redraw_sessions = redraw

    def get_deploy(self):
        return self.deploy

    def set_deploy(self, deploy):
        self.deploy = deploy

    def get_site(self):
        return self.choosed_site

    def set_site(self, site):
        self.choosed_site = site


    def get_open_sessions(self):
        return self.open_sessions

    def set_open_sessions(self, open_sessions):
        self.open_sessions = open_sessions


    def set_in_game(self, in_game):
        self.in_game = in_game

    def get_in_game(self):
        return self.in_game

    def get_login(self):
        return self.choosed_login

    def set_login(self, login):
        self.choosed_login = login

    def get_session_id(self):
        return self.session_id

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_marked_session_id(self):
        return self.marked_session_id

    def set_marked_session_id(self, session_id):
        self.marked_session_id = session_id

    def get_count_open_sessions(self):
        return len(self.open_sessions)

    def get_default_font(self):
        return self.default_font

    def get_akt_stage(self):
        return self.akt_stage

    def set_akt_stage(self, stage):
        self.akt_stage = stage

    def get_akt_phaze(self):
        return self.akt_phaze

    def set_akt_phaze(self, phaze):
        self.akt_phaze = phaze

    def get_choosed_site(self):
        return self.choosed_site

    def get_unit_id(self):
        return self.move[0][0]

    def set_unit_id(self, unitid, flag=None, hexid=None):
        self.move[0][0] = unitid
        self.move[0][1] = flag
        self.move[0][2] = hexid

    def set_unit_to_move(self, hexid):
        self.move[1] = hexid

    def set_unit_flag(self, flag):
        self.move[0][1] = flag

    def get_unit_flag(self):
        return self.move[0][1]

    def get_akt_player(self):
        return self.akt_player

    def set_akt_player(self, player):
        self.akt_player = player
