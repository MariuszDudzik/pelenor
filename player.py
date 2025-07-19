import dictionary
import pawn
import random
import time

class Player(object):
      def __init__(self, name, site, login, spell_power, socket,  picture = None):
    
        self.name = name
        self.site = site # 'C', 'Z'
        self.login = login
        self.spell_power = spell_power
        self.socket = socket
        self.picture = picture
        self.units = {}
        self.demoralization_threshold_1 = 0
        self.demoralization_threshold_2 = 0
        self.demoralization_threshold_3 = 0
        self.heads = 12
        self.last_ping_time = time.time()


      def create_army(self, site, server_con):
        army_dict = {}
        for w in dictionary.pawn:
            if site == w[4]:
                quantity = w[0]
                for _ in range(quantity):
                    unit = pawn.Pawn(w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], 
                                    w[10], w[11], w[12], w[13], w[14], w[15], w[16], w[17], 
                                    w[18], w[19], w[20], w[21], w[22])
                    unit.id = server_con.get_unit_id()
                    army_dict[unit.id] = unit

        return army_dict

       

      def to_dict(self):
        return {
            'name': self.name,
            'site': self.site,
            'login': self.login,
            'spell_power': self.spell_power,
            'picture': self.picture,
            'units': {str(unit_id): unit.to_dict() for unit_id, unit in self.units.items()},
            'heads': self.heads,
            'demoralization_thresholds': [
                self.demoralization_threshold_1,
                self.demoralization_threshold_2,
                self.demoralization_threshold_3
            ],
        }
      
      
      def from_dict(self, data):
        self.name = data.get('name')
        self.site = data.get('site')
        self.login = data.get('login')
        self.spell_power = data.get('spell_power')
        self.picture = data.get('picture')
        
        self.units = {}
        units_data = data.get('units', {})
        for unit_id_str, unit_data in units_data.items():
            unit = pawn.Pawn().from_dict(unit_data)
            unit.id = int(unit_id_str)
            self.units[unit.id] = unit

        self.heads = data.get('heads')
        demoralization_thresholds = data.get('demoralization_thresholds', [0, 0, 0])
        self.demoralization_threshold_1 = demoralization_thresholds[0]
        self.demoralization_threshold_2 = demoralization_thresholds[1]
        self.demoralization_threshold_3 = demoralization_thresholds[2]

        return self

       

      def set_units(self, units):
        self.units = units


      def get_units(self):
        return self.units
   
   
      def shuffle(self):
        unit_items = list(self.units.items())
        random.shuffle(unit_items)
        self.units = dict(unit_items)

      def get_login(self):
        return self.login

      def get_demoralization_threshold_1(self):
        return self.demoralization_threshold_1

      def get_demoralization_threshold_2(self):
        return self.demoralization_threshold_2

      def get_demoralization_threshold_3(self):
        return self.demoralization_threshold_3

      def get_spell_power(self):
        return self.spell_power

      def get_heads(self):
        return self.heads

      def set_heads(self, heads):
        self.heads = heads

      def get_site(self):
        return self.site

