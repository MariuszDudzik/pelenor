class Pawn(object):
    _id_counter = 1

    def __init__(self, name = None, nationality = None, type = None, membership = None, 
                 stageDeploy = None, forceHand = None, 
                 forceHandR = None, forceShot = None, forceShotR = None, shotRange = None, 
                 defence = None, defenceR = None, morale = None, moraleR = None, 
                 demoralizationPoint = None, authority = None, authorityR = None, 
                 spellPower = None, movement = None, isRewers = None, QRS = None, graphics = None):
        self.id = Pawn._id_counter 
        Pawn._id_counter += 1
        self.name = name
        self.nationality = nationality
        self.unitType = type  #P, J, S, D, N, M (piechota, jazda, mumakil, dowodzca, wódz naczelny, maszyna)
        self.membership = membership #C, Z (czerowny, zielony)
        self.stageDeploy = stageDeploy
        self.forceHand = forceHand  #wartosc od A-E
        self.forceHandR = forceHandR
        self.forceShot = forceShot #warosc od a-e
        self.forceShotR = forceShotR
        self.shotRange = shotRange
        self.defence = defence  #wartosc od 4-1
        self.defenceR = defenceR
        self.morale = morale  #wartosc od W-Z
        self.moraleR = moraleR
        self.demoralizationPoint = demoralizationPoint
        self.authority = authority  #autorytet wodza
        self.authorityR = authorityR
        self.spellPower = spellPower  #moc czarów naczelnego wodza
        self.movement = movement
        self.isRewers = isRewers #T, N
        self.QRS = QRS
        self.graphics = graphics
        self.surface = None
        self.coordinatesXY = None
        self.fanatic = False
        self.demoralizaztion = False
        self.rewers = False
        self.distracted = False
        self.gatherOfdistracted = 0
        self.makeMove = False
        self.castSpell = False
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
            'unitType': self.unitType,
            'membership': self.membership,
            'stageDeploy': self.stageDeploy,
            'forceHand': self.forceHand,
            'forceHandR': self.forceHandR,
            'forceShot': self.forceShot,
            'forceShotR': self.forceShotR,
            'shotRange': self.shotRange,
            'defence': self.defence,
            'defenceR': self.defenceR,
            'morale': self.morale,
            'moraleR': self.moraleR,
            'demoralizationPoint': self.demoralizationPoint,
            'authority': self.authority,
            'authorityR': self.authorityR,
            'spellPower': self.spellPower,
            'movement': self.movement,
            'isRewers': self.isRewers,
            'QRS': self.QRS,
            'graphics': self.graphics,
            'surface': self.surface,
            'coordinatesXY': self.coordinatesXY,
            'fanatic': self.fanatic,
            'demoralizaztion': self.demoralizaztion,
            'rewers': self.rewers,
            'distracted': self.distracted,
            'gatherOfdistracted': self.gatherOfdistracted,
            'makeMove': self.makeMove,
            'castSpell': self.castSpell,
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
        self.unitType = data.get('unitType')
        self.membership = data.get('membership')
        self.stageDeploy = data.get('stageDeploy')
        self.forceHand = data.get('forceHand')
        self.forceHandR = data.get('forceHandR')
        self.forceShot = data.get('forceShot')
        self.forceShotR = data.get('forceShotR')
        self.shotRange = data.get('shotRange')
        self.defence = data.get('defence')
        self.defenceR = data.get('defenceR')
        self.morale = data.get('morale')
        self.moraleR = data.get('moraleR')
        self.demoralizationPoint = data.get('demoralizationPoint')
        self.authority = data.get('authority')
        self.authorityR = data.get('authorityR')
        self.spellPower = data.get('spellPower')
        self.movement = data.get('movement')
        self.isRewers = data.get('isRewers')
        self.QRS = data.get('QRS')
        self.graphics = data.get('graphics')
        self.surface = data.get('surface')
        self.coordinatesXY = data.get('coordinatesXY')
        self.fanatic = data.get('fanatic', False)
        self.demoralizaztion = data.get('demoralizaztion', False)
        self.rewers = data.get('rewers', False)
        self.distracted = data.get('distracted', False)
        self.gatherOfdistracted = data.get('gatherOfdistracted', 0)
        self.makeMove = data.get('makeMove', False)
        self.castSpell = data.get('castSpell', False)
        self.shot = data.get('shot', False)
        self.fight = data.get('fight', False)
        self.siege = data.get('siege', False)
        self.deploy = data.get('deploy', False)
        self.tar = data.get('tar', [])
        return self
    
    def getStageDeploy(self):
        return self.stageDeploy