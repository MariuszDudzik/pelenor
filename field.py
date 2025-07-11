import pawn
import kolor

class Field(object):

    def __init__(self, QRSList = None, coulor = None, rimColourList = None, 
                 rimThicknessList = None, movementList = None, TerrainSign = None, 
                 movementPointToSpend = None, defencePoint = None, darkcoulor = None):
        self.pawnList = []
        self.pawnGraphList = []
        self.QRSList = QRSList
        self.coulor = coulor
        self.rimColourList = rimColourList
        self.rimThicknessList = rimThicknessList
        self.movementList = movementList #przejazd dla np wszyscy 
        self.TerrainSign= TerrainSign #L - las, D - droga itp
        self.movementPointToSpend =movementPointToSpend
        self.defencePoint = defencePoint
        self.darkcoulor = darkcoulor
        self.colourFlag = True

    def getRimColourList(self):
        return self.rimColourList
    
    def getRimThicknessList(self):
        return self.rimThicknessList
    
    def getColour(self):
        return self.coulor
    
    def getDarkColour(self):
        return self.darkcoulor
    
    def getCoulorFlag(self):
        return self.colourFlag
    
    def getQRS(self):
        return self.QRSList
    
    def setColourFlag(self, flag):
        self.colourFlag = flag
    
    def to_dict(self):
        field_dict = {
            #'pawnList': [unit.to_dict() for unit in self.pawnList], - dla obiektow
            'pawnList': self.pawnList,
            'QRSList': self.QRSList,
            'coulor': self.coulor,
            'rimColourList': self.rimColourList,
            'rimThicknessList': self.rimThicknessList,
            'movementList': self.movementList,
            'TerrainSign': self.TerrainSign,
            'movementPointToSpend': self.movementPointToSpend,
            'defencePoint': self.defencePoint,
            'darkcoulor': self.darkcoulor,
            'colourFlag': self.colourFlag
        }
        return field_dict
    
    def from_dict(self, data):
        self.pawnList = data.get('pawnList', [])
        #self.pawnList = [pawn.Pawn().from_dict(unit_data) for unit_data in data.get('pawnList', [])] - dla obiektow
        self.QRSList = data.get('QRSList')
        self.coulor = data.get('coulor')
        self.rimColourList = data.get('rimColourList')
        self.rimThicknessList = data.get('rimThicknessList')
        self.movementList = data.get('movementList')
        self.TerrainSign = data.get('TerrainSign')
        self.movementPointToSpend = data.get('movementPointToSpend')
        self.defencePoint = data.get('defencePoint')
        self.darkcoulor = data.get('darkcoulor')
        self.colourFlag = data.get('colourFlag')

        return self