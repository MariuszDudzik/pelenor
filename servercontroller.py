class ServerController():
    def __init__(self):
        self.unitID = 1
        self.aktStage = 0
        self.aktPhaze = 0
        self.aktplayer = 'C'
        self.deploy = True

    def getUnitId(self):
        unitID = self.unitID
        self.unitID += 1
        return unitID
    
  
        

 