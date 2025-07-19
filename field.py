import pawn
import kolor

class Field(object):

    def __init__(self, qrs_list = None, colour = None, rim_colour_list = None, 
                 rim_thickness_list = None, movement_list = None, terrain_sign = None, 
                 movement_point_to_spend = None, defence_point = None, dark_colour = None):
        self.pawn_list = []
        self.pawn_graph_list = []
        self.qrs_list = qrs_list
        self.colour = colour
        self.rim_colour_list = rim_colour_list
        self.rim_thickness_list = rim_thickness_list
        self.movement_list = movement_list #przejazd dla np wszyscy 
        self.terrain_sign = terrain_sign #L - las, D - droga itp
        self.movement_point_to_spend = movement_point_to_spend
        self.defence_point = defence_point
        self.dark_colour = dark_colour
        self.colour_flag = True

    def get_rim_colour_list(self):
        return self.rim_colour_list

    def get_rim_thickness_list(self):
        return self.rim_thickness_list

    def get_colour(self):
        return self.colour

    def get_dark_colour(self):
        return self.dark_colour

    def get_colour_flag(self):
        return self.colour_flag

    def get_qrs(self):
        return self.qrs_list

    def set_colour_flag(self, flag):
        self.colour_flag = flag

    def get_terrain_sign(self):
        return self.terrain_sign

    def to_dict(self):
        field_dict = {
            #'pawnList': [unit.to_dict() for unit in self.pawnList], - dla obiektow
            'pawn_list': self.pawn_list,
            'qrs_list': self.qrs_list,
            'colour': self.colour,
            'rim_colour_list': self.rim_colour_list,
            'rim_thickness_list': self.rim_thickness_list,
            'movement_list': self.movement_list,
            'terrain_sign': self.terrain_sign,
            'movement_point_to_spend': self.movement_point_to_spend,
            'defence_point': self.defence_point,
            'dark_colour': self.dark_colour,
            'colour_flag': self.colour_flag
        }
        return field_dict
    
    def from_dict(self, data):
        self.pawn_list = data.get('pawn_list', [])
        #self.pawnList = [pawn.Pawn().from_dict(unit_data) for unit_data in data.get('pawnList', [])] - dla obiektow
        self.qrs_list = data.get('qrs_list')
        self.colour = data.get('colour')
        self.rim_colour_list = data.get('rim_colour_list')
        self.rim_thickness_list = data.get('rim_thickness_list')
        self.movement_list = data.get('movement_list')
        self.terrain_sign = data.get('terrain_sign')
        self.movement_point_to_spend = data.get('movement_point_to_spend')
        self.defence_point = data.get('defence_point')
        self.dark_colour = data.get('dark_colour')
        self.colour_flag = data.get('colour_flag')

        return self