class Field(object):

    def __init__(self, QRSList, coulor, rimColourList, rimThicknessList, 
                 movementList, TerrainSign, movementPointToSpend, defencePoint):
        self.pawnList = []
        self.QRSList = QRSList
        self.coulor = coulor
        self.rimColourList = rimColourList
        self.rimThicknessList = rimThicknessList
        self.movementList = movementList #przejazd dla np wszyscy 
        self.TerrainSign= TerrainSign #L - las, D - droga itp
        self.movementPointToSpend =movementPointToSpend
        self.defencePoint = defencePoint

    def to_dict(self):
        field_dict = {
            'pawnList': self.pawnList,
            'QRSList': self.QRSList,
            'coulor': self.coulor,
            'rimColourList': self.rimColourList,
            'rimThicknessList': self.rimThicknessList,
            'movementList': self.movementList,
            'TerrainSign': self.TerrainSign,
            'movementPointToSpend': self.movementPointToSpend,
            'defencePoint': self.defencePoint
        }
        return field_dict
    
    def from_dict(self, data):
        self.pawnList = data.get('pawnList', [])
        self.QRSList = data.get('QRSList')
        self.coulor = data.get('coulor')
        self.rimColourList = data.get('rimColourList')
        self.rimThicknessList = data.get('rimThicknessList')
        self.movementList = data.get('movementList')
        self.TerrainSign = data.get('TerrainSign')
        self.movementPointToSpend = data.get('movementPointToSpend')
        self.defencePoint = data.get('defencePoint')
        return self