
class MessageFromServer(object):
    def __init__(self, gameController, game):
        self.gameController = gameController
        self.game = game


    def serverResponseHandle(self, data):
        if 'action' in data:
            action = data['action']      
            match action:
                case 'game_created':
                    self.gameCreated(data)
                case 'list_sessions':
                    self.listSessions(data)
                case 'joined_game':
                    self.joinedGame(data)
                case 'start_game':
                    self.startGame(data)


    def gameCreated(self, data):
        if 'sessionID' in data:
            self.gameController.setSessionID(data['sessionID'])
            self.listSessions(data)
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
        player_data = data['data']['playerW']
        self.game.playerW.from_dict(player_data)
        player_data = data['data']['playerS']
        self.game.playerS.from_dict(player_data)
        player_date = data['data']['board']
        self.game.board.from_dict(player_date)
        print("Gra rozpoczęta")
      #  self.gameController.setInGame(True)


