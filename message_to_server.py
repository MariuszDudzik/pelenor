import json

class MessageToServer(object):
    def __init__(self, gameController, game):
        self.gameController = gameController
        self.game = game

    def _sendRequest(self, action, payload, clientSocket):
        request = json.dumps({
            'action': action,
            **payload  # Łączy zawartość słownika `payload` z akcją
        })
        clientSocket.sendall(request.encode()) 
     
    
    def createGame(self, clientSocket): 
        payload = {
        'login': self.gameController.getLogin(),
        'site': self.gameController.getSite()
        }
        self._sendRequest('create_game', payload, clientSocket)


    def listSessions(self, clientSocket):
        payload = {}
        self._sendRequest('list_sessions', payload, clientSocket)


    def joinGame(self, clientSocket):
        payload = {
            'sessionID': self.gameController.getMarkedSessionID(),
            'login': self.gameController.getLogin()
        }
        self._sendRequest('join_game', payload, clientSocket)