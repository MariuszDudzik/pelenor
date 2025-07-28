

class ServerController():
    def __init__(self):
        self.unit_id = 1
        self.akt_stage = 0
        self.akt_phaze = 0
        self.akt_player = 'C'
        self.deploy = True
        self.minas_tirith_dict = None

    def get_unit_id(self):
        unit_id = self.unit_id
        self.unit_id += 1
        return unit_id

    def get_akt_stage(self):
        return self.akt_stage

    def set_akt_stage(self, stage):
        self.akt_stage = stage

    def get_akt_phaze(self):
        return self.akt_phaze

    def set_akt_phaze(self, phaze):
        self.akt_phaze = phaze

    def get_akt_player(self):
        return self.akt_player

    def set_akt_player(self, player):
        self.akt_player = player

    def get_deploy(self):
        return self.deploy

    def set_deploy(self, deploy):
        self.deploy = deploy

    def set_minas_tirith_dict(self, minas_tirith_dict):
        self.minas_tirith_dict = minas_tirith_dict

    def get_minas_tirith_dict(self):
        return self.minas_tirith_dict

 