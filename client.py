import socket
import json
import time
import message_from_server
import message_to_server

class Client(object):
    def __init__(self, gameController, game):
        self.clientSocket = None
        self.serverAddress = None
        self.port = None
        self.action = None
        self.connectionStatus = ""
       # self.gameController = gameController
        self.messageFromServer = message_from_server.MessageFromServer(gameController, game)
        self.messageToServer = message_to_server.MessageToServer(gameController, game)

        self._loadServerAddress()
 

    def _loadServerAddress(self):
        with open("server.dat", "r") as file:
            self.serverAddress = file.readline().strip()  
            self.port = int(file.readline().strip())


    def startConnection(self):
        server_address = (self.serverAddress, self.port)
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clientSocket.connect(server_address)
            self.setConnectionStatus("Połączono z serwerem")
        except Exception as e:
            self.setConnectionStatus(f"Błąd połączenia: {e}")
            self.setSocket(None)


    def getsocket(self):
        return self.clientSocket
    

    def setSocket(self, nowSocket):
        self.clientSocket = nowSocket
    

    def close_connection(self):
        if self.clientSocket:
            try:
                self.clientSocket.close()
            except OSError:
                pass 
            finally:
                self.setSocket(None)

    
    def getAction(self):
        return self.action
    

    def setAction(self, action):
        self.action = action

    def getConnectionStatus(self):
        return self.connectionStatus
    
    
    def setConnectionStatus(self, connectionStatus):
        self.connectionStatus = connectionStatus


    def pingServer(self):
        while True:
            try:
                pingData = json.dumps({'action': 'ping'})
                self.clientSocket.send(pingData.encode('utf-8'))
                time.sleep(5)
            except Exception as e:
                print(f"Błąd podczas pingowania: {e}")
                break


    def receiveData(self):
        while True:            
            try:
                response = self.clientSocket.recv(1024).decode()
                if response:
                    data = json.loads(response)
                    self.serverResponseHandle(data)
            except Exception as e:
                print(f"Błąd odbierania danych: {e}")
                break


    def serverResponseHandle(self, data):
        if 'action' in data:
            action = data['action']
            if action == 'game_created':
                self.setConnectionStatus(self.messageFromServer.gameCreated(data))
            elif action == 'list_sessions':
                self.messageFromServer.listSessions(data)
            elif action == 'joined_game':
                self.messageFromServer.joinedGame(data)
            elif action == 'start_game':
                print("Gra rozpoczęta")
        #        self.messageFromServer.startGame(data)


    def gameClient(self):
        if self.getAction():
            if self.getAction() == 'create_game':
                self.messageToServer.createGame(self.getsocket())
                self.messageToServer.listSessions(self.getsocket())
            elif self.getAction() == 'list_sessions':
                self.messageToServer.listSessions(self.getsocket())
            elif self.getAction() == 'join_game':
                self.messageToServer.joinGame(self.getsocket())


