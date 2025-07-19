import dictionary as dictionary
import field

class Board(object):
    def __init__(self):
        self.hexes = {}
        self._addHex()


    def _addHex(self):
        for w in dictionary.field: 
            self.hexes[w[1]] = field.Field(w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], self.set_dark_colour(w[2]))
                                           

    def to_dict(self):
        return {
            'hexes': {
                f"{k[0]},{k[1]},{k[2]}": hex_.to_dict()
                for k, hex_ in self.hexes.items()
            }
        }
    

    def from_dict(self, data):
        hexes_data = data.get('hexes', {})
        self.hexes = {}

        for key_str, hex_data in hexes_data.items():
            q, r, s = map(int, key_str.split(','))
            self.hexes[(q, r, s)] = field.Field().from_dict(hex_data)

        return self
    

    def get_hexes(self):
        return self.hexes
    

    def set_dark_colour(self, w):
        colour_map = {
            'Y': 'PY',
            'G': 'PG',
            'Z': 'PZ',
            'W': 'PW',
            'T': 'PT',
            'K': 'PK',
            'S': 'PS',
            'O': 'PO',
            'B': 'B'
        }
        if w in colour_map:
            return colour_map[w]
        else:
            return 'B'