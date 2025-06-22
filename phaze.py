import kolor
import dictionary as dictionary

class Phaze(object):
    def __init__(self, nrstage = 0, nrphaze = 0, colour = None, name = None):
        self.nrStage = nrstage
        self.nrPhaze = nrphaze
        self.colour = colour
        self.name = name
        self.completed = False

    def getColour(self):
        return self.colour
    
    def getName(self):
        return self.name
    
    def getNrStage(self):
        return self.nrStage
    
    def getNrPhaze(self):
        return self.nrPhaze

def createPhaze():
    list = []
    for j in range(0, 16):
        for i in range(1, 9):
            name = dictionary.phaze[i]
            obj = Phaze(j + 1, i, kolor.GREY, name)
            list.append(obj)
    return list


