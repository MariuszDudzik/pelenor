import dictionary
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
        self.units = {}
        self.demoralizationTreshold1 = 0
        self.demoralizationTreshold2 = 0
        self.demoralizationTreshold3 = 0
        self.heads = 12
        self.lastPingTime = time.time()


      def createArmy(self, site):
        army_dict = {}

        for w in dictionary.pawn:
            if site == w[4]:
                quantity = w[0]
                for _ in range(quantity):
                    unit = pawn.Pawn(w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], 
                                    w[10], w[11], w[12], w[13], w[14], w[15], w[16], w[17], 
                                    w[18], w[19], w[20], w[21], w[22])
                    army_dict[unit.id] = unit

        return army_dict

       

      def to_dict(self):
        return {
            'name': self.name,
            'site': self.site,
            'login': self.login,
            'spellPower': self.spellPower,
            'picture': self.picture,
            'units': {str(unit_id): unit.to_dict() for unit_id, unit in self.units.items()},
            'heads': self.heads,
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
        
        self.units = {}
        units_data = data.get('units', {})
        for unit_id_str, unit_data in units_data.items():
            unit = pawn.Pawn().from_dict(unit_data)
            unit.id = int(unit_id_str)
            self.units[unit.id] = unit

        self.heads = data.get('heads')
        demoralization_thresholds = data.get('demoralizationThresholds', [0, 0, 0])
        self.demoralizationThreshold1 = demoralization_thresholds[0]
        self.demoralizationThreshold2 = demoralization_thresholds[1]
        self.demoralizationThreshold3 = demoralization_thresholds[2]
        
        return self

       

      def setUnits(self, units):
        self.units = units


      def getUnits(self):
        return self.units
   
   
      def shuffle(self):
        unit_items = list(self.units.items())
        random.shuffle(unit_items)
        self.units = dict(unit_items)

      def getLogin(self):
        return self.login
      
      def getDemoralizationTreshold1(self):
        return self.demoralizationTreshold1
      
      def getDemoralizationTreshold2(self):
        return self.demoralizationTreshold2
      
      def getDemoralizationTreshold3(self):
        return self.demoralizationTreshold3
      
      def getSpellPower(self):
        return self.spellPower

      def getHeads(self):
        return self.heads
      
      def setHeads(self, heads):
        self.heads = heads
