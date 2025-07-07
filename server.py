import socket
import threading
import json
from collections import defaultdict
import time
import server_data_handler
import struct
import servercontroller
import gamelogic

class GameServer:
    def __init__(self):
        self.sessions = defaultdict(dict)  # Każda sesja przechowuje graczy i stan gry
        self.nextSessionID = 1             # ID do śledzenia unikalnych sesji
        self.lock = threading.Lock()       # Lock do synchronizacji dostępu do sesji
        self.messageFromClient = server_data_handler.MessageFromClient()
   
  
    def _sendJson(self, clientSocket, data):
        if not isinstance(data, dict):
            return
        json_string = json.dumps(data)  
        request_bytes = json_string.encode('utf-8')  
        request_length = len(request_bytes)
        clientSocket.sendall(struct.pack('!I', request_length))
        clientSocket.sendall(request_bytes)


    def clientHandler(self, clientSocket):
        try:
            while True:
                length_data = b""
                while len(length_data) < 4:
                    packet = clientSocket.recv(4 - len(length_data))
                    if not packet:
                        return
                    length_data += packet

                response_length = struct.unpack('!I', length_data)[0]
                received_data = b""
                while len(received_data) < response_length:
                    packet = clientSocket.recv(min(4096, response_length - len(received_data)))
                    if not packet:
                        raise ConnectionError("Połączenie zerwane w trakcie odbierania danych.")
                    received_data += packet

                data = json.loads(received_data.decode())
                self.handleAction(clientSocket, data)

        except Exception as e:
            print(f"Błąd odbioru danych: {e}")
            

    def handleAction(self, clientSocket, data):
        action = data.get('action')     
        match action:
            case 'create_game':
                with self.lock:
                    sessionID = self.nextSessionID
                    serverCon = servercontroller.ServerController()
                    player_, board_ = self.messageFromClient.create_game(clientSocket, data, serverCon)
                    self.sessions[sessionID] = {'players': [player_], 'plansza': board_, 'handler': serverCon}
                    self.nextSessionID += 1
                    print(f"Sesja {sessionID} utworzona przez {player_.login}.")
                    sessions = self.messageFromClient.openSessionsGame(self.sessions)
                    self._sendJson(clientSocket, {'action': 'game_created', 'sessionID': sessionID, 'sessions': sessions})        
            case 'list_sessions':
                with self.lock:
                    sessions = self.messageFromClient.openSessionsGame(self.sessions)
                    self._sendJson(clientSocket, {'action': 'list_sessions', 'sessions': sessions})         
            case 'join_game':
                with self.lock:
                    sessionID = data.get('sessionID')
                    if sessionID not in self.sessions:
                        self._sendJson(clientSocket, {'action': 'joined_game', 'error': 'Session not found'})
                    elif self.messageFromClient.isFull(self.sessions, sessionID):
                        self._sendJson(clientSocket, {'action': 'joined_game', 'error': 'Session is full'})
                    else:
                        player_ = self.messageFromClient.prepareSecondPlayer(clientSocket, data, self.sessions)
                        self.sessions[sessionID]['players'].append(player_)
                        gamelogic.GameLogic.S_deploy_palace_gward(self.sessions[sessionID]['plansza'], self.sessions[sessionID]['players'])
                        print(f"Gracz {player_.login} dołączył do sesji {sessionID}.")
                        self._sendJson(clientSocket, {'action': 'joined_game', 'sessionID': sessionID})       
                        parcel = self.messageFromClient.startGame(self.sessions[sessionID]['players'], 
                                                                  self.sessions[sessionID]['plansza'])
                        for player in self.sessions[sessionID]['players']:
                            self._sendJson(player.socket, {'action': 'start_game', 'data': parcel})      
            case 'ping':
                with self.lock:
                    sessionID = data.get('sessionID')
                    if sessionID != None:
                        try:
                            for player in self.sessions[sessionID]['players']:
                                if player.socket == clientSocket:
                                    player.lastPingTime = time.time() 
                        except:
                            print(f"Brak sesji {sessionID}")         
            case _:
                print(f"Nieznana akcja: {action}")
                    

    def playerLastPing(self):
        while True:
            with self.lock:
                for sessionID, sessionData in list(self.sessions.items()):
                    for player in list(sessionData['players']):
                        if time.time() - player.lastPingTime > 30:
                            print(f"Gracz {player.login} nie odpowiada. Usuwam go z sesji {sessionID}")
                            sessionData['players'].remove(player)
                    
                    if len(sessionData['players']) == 0:
                        del self.sessions[sessionID]
                        print(f"Sesja {sessionID} została automatycznie usunięta (brak graczy).")
            time.sleep(5)


def startServer():
    gameServer = GameServer()
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('0.0.0.0', 25565))
    serverSocket.listen(100)
    print("Serwer oczekuje na połączenia...")
    threading.Thread(target=gameServer.playerLastPing, daemon=True).start()

    while True:
        clientSocket, addr = serverSocket.accept()
        print(f"Połączono z {addr}")
        threading.Thread(target=gameServer.clientHandler, args=(clientSocket,)).start()

if __name__ == "__main__":
    startServer()
