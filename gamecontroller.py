import platform

class GameController(object):
    def __init__(self):
        self.inGame = False
        self.sessionID = None
        self.markedSessionID = None
        self.choosedSite = None
        self.choosedLogin = None
        self.openSessions = []
        self.system = platform.system()
        self.defaultFont = None
        
        self._setDefaultFont()


    def _setDefaultFont(self):
        if self.system == 'Windows':
            self.defaultFont = 'Arial'
        elif self.system == 'Linux':
            self.defaultFont = 'Liberation Sans'
        else:
            self.defaultFont = 'None'
  
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