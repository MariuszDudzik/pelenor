import kolor
import dictionary as dictionary

class Phaze(object):
    def __init__(self, nr_stage = 0, nr_phaze = 0, colour = None, name = None):
        self.nr_stage = nr_stage
        self.nr_phaze = nr_phaze
        self.colour = colour
        self.name = name
        self.completed = False

    def get_colour(self):
        return self.colour

    def get_name(self):
        return self.name

    def get_nr_stage(self):
        return self.nr_stage

    def get_nr_phaze(self):
        return self.nr_phaze

def create_phaze():
    list = []
    for j in range(0, 16):
        for i in range(1, 9):
            name = dictionary.phaze[i]
            obj = Phaze(j + 1, i, kolor.GREY, name)
            list.append(obj)
    return list


