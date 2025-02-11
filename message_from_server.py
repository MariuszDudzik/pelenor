import json
import game

class MessageFromServer(object):
    def __init__(self, gameController, game):
        self.gameController = gameController
        self.game = game

    def gameCreated(self, data):
        if 'sessionID' in data:
            self.gameController.setSessionID(data['sessionID'])
            return ("Czekam na dołączenie drugiego gracza...")
        else:
            return (f"Błąd przy tworzeniu gry: {data.get('error', 'Nieznany błąd')}")
        

    def listSessions(self, data):
            self.gameController.setOpenSessions(data['sessions'])


    def joinedGame(self, data):
        if 'sessionID' in data:
            self.gameController.setSessionID(data['sessionID'])
            print(f"Dołączono do gry: {self.gameController.getSessionID()}")
        else:
            print(f"Nie można dołączyć do gry: {data.get('error', 'Nieznany błąd')}")

    def startGame(self, data):
        print("Gra rozpoczęta2")
        self.game.playerW.from_dict(data['playerW'])
        self.game.playerS.from_dict(data['playerS'])
      #  self.game.board.from_dict(data['board'])
        self.gameController.setInGame(True)

