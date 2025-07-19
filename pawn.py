class Pawn(object):

    def __init__(self, name = None, nationality = None, type = None, membership = None, 
                 stage_deploy = None, force_hand = None, 
                 force_hand_r = None, force_shot = None, force_shot_r = None, shot_range = None, 
                 defence = None, defence_r = None, morale = None, morale_r = None, 
                 demoralization_point = None, authority = None, authority_r = None, 
                 spell_power = None, movement = None, is_rewers = None, qrs = None, graphics = None):
        self.id = 0
        self.name = name
        self.nationality = nationality
        self.unit_type = type  #P, J, S, D, N, M (piechota, jazda, mumakil, dowodzca, wódz naczelny, maszyna)
        self.membership = membership #C, Z (czerowny, zielony)
        self.stage_deploy = stage_deploy
        self.force_hand = force_hand  #wartosc od A-E
        self.force_hand_r = force_hand_r
        self.force_shot = force_shot  #warosc od a-e
        self.force_shot_r = force_shot_r
        self.shot_range = shot_range
        self.defence = defence  #wartosc od 4-1
        self.defence_r = defence_r
        self.morale = morale  #wartosc od W-Z
        self.morale_r = morale_r
        self.demoralization_point = demoralization_point
        self.authority = authority  #autorytet wodza
        self.authority_r = authority_r
        self.spell_power = spell_power  #moc czarów naczelnego wodza
        self.movement = movement
        self.akt_movement = movement
        self.is_rewers = is_rewers #T, N
        self.qrs = qrs
        self.graphics = graphics
        self.surface = None
        self.coordinates_xy = None
        self.fanatic = False
        self.demoralization = False
        self.rewers = False
        self.distracted = False
        self.gather_of_distracted = 0
        self.make_move = False
        self.cast_spell = False
        self.shot = False
        self.fight = False
        self.siege = False
        self.deploy = False
        self.tar = [] #'T', 'F' smoła

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nationality': self.nationality,
            'unit_type': self.unit_type,
            'membership': self.membership,
            'stage_deploy': self.stage_deploy,
            'force_hand': self.force_hand,
            'force_hand_r': self.force_hand_r,
            'force_shot': self.force_shot,
            'force_shot_r': self.force_shot_r,
            'shot_range': self.shot_range,
            'defence': self.defence,
            'defence_r': self.defence_r,
            'morale': self.morale,
            'morale_r': self.morale_r,
            'demoralization_point': self.demoralization_point,
            'authority': self.authority,
            'authority_r': self.authority_r,
            'spell_power': self.spell_power,
            'movement': self.movement,
            'akt_movement': self.akt_movement,
            'is_rewers': self.is_rewers,
            'qrs': self.qrs,
            'graphics': self.graphics,
            'surface': self.surface,
            'coordinates_xy': self.coordinates_xy,
            'fanatic': self.fanatic,
            'demoralization': self.demoralization,
            'rewers': self.rewers,
            'distracted': self.distracted,
            'gather_of_distracted': self.gather_of_distracted,
            'make_move': self.make_move,
            'cast_spell': self.cast_spell,
            'shot': self.shot,
            'fight': self.fight,
            'siege': self.siege,
            'deploy': self.deploy,
            'tar': self.tar
        }
    
    def from_dict(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.nationality = data.get('nationality')
        self.unit_type = data.get('unit_type')
        self.membership = data.get('membership')
        self.stage_deploy = data.get('stage_deploy')
        self.force_hand = data.get('force_hand')
        self.force_hand_r = data.get('force_hand_r')
        self.force_shot = data.get('force_shot')
        self.force_shot_r = data.get('force_shot_r')
        self.shot_range = data.get('shot_range')
        self.defence = data.get('defence')
        self.defence_r = data.get('defence_r')
        self.morale = data.get('morale')
        self.morale_r = data.get('morale_r')
        self.demoralization_point = data.get('demoralization_point')
        self.authority = data.get('authority')
        self.authority_r = data.get('authority_r')
        self.spell_power = data.get('spell_power')
        self.movement = data.get('movement')
        self.akt_movement = data.get('akt_movement')
        self.is_rewers = data.get('is_rewers')
        self.qrs = data.get('qrs')
        self.graphics = data.get('graphics')
        self.surface = data.get('surface')
        self.coordinates_xy = data.get('coordinates_xy')
        self.fanatic = data.get('fanatic', False)
        self.demoralization = data.get('demoralization', False)
        self.rewers = data.get('rewers', False)
        self.distracted = data.get('distracted', False)
        self.gather_of_distracted = data.get('gather_of_distracted', 0)
        self.make_move = data.get('make_move', False)
        self.cast_spell = data.get('cast_spell', False)
        self.shot = data.get('shot', False)
        self.fight = data.get('fight', False)
        self.siege = data.get('siege', False)
        self.deploy = data.get('deploy', False)
        self.tar = data.get('tar', [])
        return self

    def get_stage_deploy(self):
        return self.stage_deploy

    def get_site(self):
        return self.membership

    def get_deploy(self):
        return self.deploy

    def set_deploy(self):
        self.deploy = True

    def set_qrs(self, qrs):
        self.qrs = qrs

    def get_qrs(self):
        return self.qrs

    def get_id(self):
        return self.id

    def get_distracted(self):
        return self.distracted

    def get_unit_type(self):
        return self.unit_type