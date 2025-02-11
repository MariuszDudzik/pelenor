import dict
import pawn
import random
import time

class Player(object):
      def __init__(self, name, site, login, spellPower, socket,  picture = None):
    
        self.name = name
        self.site = site # 'C', 'Z'
        self.login = login
        self.spellPower = spellPower
        self.socket = socket
        self.picture = picture
        self.units = []
        self.demoralizationTreshold1 = 0
        self.demoralizationTreshold2 = 0
        self.demoralizationTreshold3 = 0
        self.lastPingTime = time.time()


      def createArmy(self, site):
        listOfArmy = []
        for w in dict.pawn:
            if site == w[4]:
                quantity = w[0]
                for i in range(quantity):
                    unit = pawn.Pawn(w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], 
                                        w[10], w[11], w[12], w[13], w[14], w[15], w[16], w[17], 
                                        w[18], w[19], w[20], w[21], w[22])
                    listOfArmy.append(unit)
        return listOfArmy
      

      def to_dict(self):
        return {
            'name': self.name,
            'site': self.site,
            'login': self.login,
            'spellPower': self.spellPower,
            'picture': self.picture,
            'units': [unit.to_dict() for unit in self.units],
            'demoralizationTresholds': [
                self.demoralizationTreshold1,
                self.demoralizationTreshold2,
                self.demoralizationTreshold3
            ],
        }
      
      def from_dict(self, data):
        self.name = data.get('name')
        self.site = data.get('site')
        self.login = data.get('login')
        self.spellPower = data.get('spellPower')
        self.picture = data.get('picture')
        self.units = [pawn.Pawn().from_dict(unit_data) for unit_data in data.get('units', [])]
        demoralizationTresholds = data.get('demoralizationTresholds', [0, 0, 0])
        self.demoralizationTreshold1, self.demoralizationTreshold2, self.demoralizationTreshold3 = demoralizationTresholds
        return self
       


      def setUnits(self, units):
        self.units = units


      def getUnits(self):
        return self.units

     
      def shuffle(self):
        random.shuffle(self.units)

        
