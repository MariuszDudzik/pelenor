import platform

class GameController(object):
    def __init__(self):
        self.inGame = True
        self.sessionID = None
        self.markedSessionID = None
        self.choosedSite = None
        self.choosedLogin = None
        self.openSessions = []
        self.system = platform.system()
        self.defaultFont = None
        self.aktStage = 0
        self.aktPhaze = 0
        self.aktplayer = 'C'
        self.deploy = True
        
        self._setDefaultFont()


    def _setDefaultFont(self):
        if self.system == 'Windows':
            self.defaultFont = 'Arial'
        elif self.system == 'Linux':
            self.defaultFont = 'Liberation Sans'
        else:
            self.defaultFont = 'None'
  
    def getRedrawSessions(self):
        return self.redrawSessions
    
    def setRedrawSessions(self, redraw):
        self.redrawSessions = redraw

    def getDeploy(self):
        return self.deploy
    
    def setDeploy(self, deploy):
        self.deploy = deploy

    def getSite(self):
        return self.choosedSite
    
    def setSite(self, site):
        self.choosedSite = site


    def getOpenSessions(self):
        return self.openSessions
    
    def setOpenSessions(self, openSessions):
        self.openSessions = openSessions


    def setInGame(self, inGame):
        self.inGame = inGame

    def getInGame(self):
        return self.inGame
    
    def getLogin(self):
        return self.choosedLogin
    
    def setLogin(self, login):
        self.choosedLogin = login

    def getSessionID(self):
        return self.sessionID
    
    def setSessionID(self, sessionID):
        self.sessionID = sessionID

    def getMarkedSessionID(self):
        return self.markedSessionID
    
    def setMarkedSessionID(self, sessionID):
        self.markedSessionID = sessionID

    def getCountOpenSessions(self):
        return len(self.openSessions)
    
    def getDefaultFont(self):
        return self.defaultFont
    
    def getAktStage(self):
        return self.aktStage
    
    def getChoosedSite(self):
        return self.choosedSite
    