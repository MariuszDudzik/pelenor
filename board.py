import dict
import field

class Board(object):
    def __init__(self):
        self.hexes = {}

        self._addHex()


    def _addHex(self):
        for w in dict.field: 
            self.hexes[w[0]] = field.Field(w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8])


    def to_dict(self):
        return {
            'hexes': {key: hex_.to_dict() for key, hex_ in self.hexes.items()} 
        }
    

    def from_dict(self, data):
        hexes_data = data.get('hexes', {})
        self.hexes = {key: field.Field().from_dict(hex_data) for key, hex_data in hexes_data.items()}
        return self

