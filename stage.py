import dictionary as dictionary
import kolor

class Stage(object):
    def __init__(self, nr = 0, colour = None, season = None, text = None):
        self.nrStage = nr
        self.colour = colour
        self.season = season
        self.text = text

    def getColour(self):
        return self.colour

    def getSeason(self):
        return self.season

    def getText(self):
        return self.text
    
    def getNrStage(self):
        return self.nrStage


def createStage():
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


    