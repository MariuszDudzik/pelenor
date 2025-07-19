import dictionary as dictionary
import kolor

class Stage(object):
    def __init__(self, nr = 0, colour = None, season = None, text = None):
        self.nr_stage = nr
        self.colour = colour
        self.season = season
        self.text = text

    def get_colour(self):
        return self.colour

    def get_season(self):
        return self.season

    def get_text(self):
        return self.text

    def get_nr_stage(self):
        return self.nr_stage


def create_stage():
    list = []
    for i in range(1, 17):
        season = dictionary.stage[i][0]
        text = dictionary.stage[i][1]
        if i >= 2 and i <= 6:
            colour = kolor.PERU
        else:
            colour = kolor.YELLOW
        obj = Stage(i, colour, season, text)
        list.append(obj)
    return list


    