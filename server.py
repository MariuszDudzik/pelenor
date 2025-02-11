import socket
import threading
import json
from collections import defaultdict
import time
import server_data_handler


class GameServer:
    def __init__(self):
        self.sessions = defaultdict(dict)  # Każda sesja to klucz sesji z listą graczy i stanem gry
        self.nextSessionID = 1           # ID do śledzenia unikalnych sesji
        self.lock = threading.Lock()       # Lock do synchronizacji dostępu do sesji
        self.messageFromClient = server_data_handler.MessageFromClient()


    def sendJson(sock, data, chunk_size=1024):
        json_data = json.dumps(data, ensure_ascii=False)
        total_length = len(json_data)
        
        sock.sendall(f"{total_length}\n".encode('utf-8'))

        for i in range(0, total_length, chunk_size):
            chunk = json_data[i:i + chunk_size] 
            sock.sendall(chunk.encode('utf-8'))

     
    def removePlayerFromSession(self, clientSocket):
        with self.lock:
            for sessionID, sessionData in list(self.sessions.items()):
                for player in sessionData['players']:
                    if player.socket == clientSocket:
                        sessionData['players'].remove(player)
                        print(f"Gracz {player.login} został usunięty z sesji {sessionID}")
                   

    def graczeLastPing(self):
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

    
    def clientHandler(self, clientSocket):
        try:
            while True:
                
                message = clientSocket.recv(1024).decode()
                if not message:
                    break
                data = json.loads(message)

                if data['action'] == 'create_game':
                    with self.lock:
                        sessionID = self.nextSessionID
                        player_, board_ = self.messageFromClient.create_game(clientSocket, data)
                        self.sessions[sessionID] = {'players':[player_], 'plansza': board_}
                        self.nextSessionID += 1           
                        print(f"Nowa sesja gry {sessionID} została utworzona przez {player_.login} jako {player_.name}")
                        response = json.dumps({'action': 'game_created', 'sessionID': sessionID})
                        clientSocket.sendall(response.encode())
      
                elif data['action'] == 'list_sessions':
                    with self.lock:
                        sessions = self.messageFromClient.openSessionsGame(self.sessions)
                        response = json.dumps({'action': 'list_sessions', 'sessions': sessions})
                        clientSocket.sendall(response.encode())

                elif data['action'] == 'join_game':
                    with self.lock:
                        sessionID = data.get('sessionID')
                        if sessionID not in self.sessions:
                            response = json.dumps({'action': 'joined_game', 'error': 'Session not found'})
                        else:
                            if self.messageFromClient.isFull(self.sessions, sessionID):
                                response = json.dumps({'action': 'joined_game', 'error': 'Session is full'})
                            else:
                                player_ = self.messageFromClient.prepareSecondPlayer(clientSocket, data, self.sessions)
                                self.sessions[sessionID]['players'].append(player_) 
                                print(f"Gracz {player_.login} dołączył do gry jako {player_.name}.")
                       # else:
                       #         print(f"Błąd: {player_['data']}")
                                response = json.dumps({'action': 'joined_game', 'sessionID': sessionID})
                                clientSocket.sendall(response.encode())

                             #   if len(self.sessions[sessionID]['players']) == 2:
                                parcel = self.messageFromClient.startGame(self.sessions[sessionID]['players'], self.sessions[sessionID]['plansza'])
                                response = json.dumps({'action': 'start_game', 'data': parcel}, ensure_ascii=False)
                                total_length = len(response)

                               # response = response.encode()
                               # data2 = json.loads(response.decode())
                                #data = json.loads(response)
                              #  print(json.dumps(data2, indent=4))
                                clientSocket.sendall(response.encode())

                               # for player in self.sessions[sessionID]['players']:
                               #     player.socket.sendall(response.encode())
                                   
                                   

                elif data['action'] == 'ping':
                    with self.lock:
                        for sessionID, sessionData in self.sessions.items():
                            for player in sessionData['players']:
                                if player.socket == clientSocket:
                                    player.lastPingTime = time.time()
                                    break

        except ConnectionResetError:
            print("Klient się rozłączył")
            self.removePlayerFromSession(clientSocket)
        finally:
            clientSocket.close()
            
          

def startServer():
    gameServer = GameServer()
   
    # Konfiguracja serwera TCP
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('0.0.0.0', 25565))
    serverSocket.listen(100)  # Maksymalnie 100 oczekujących połączeń
    print("Serwer oczekuje na połączenia...")
    threading.Thread(target=gameServer.graczeLastPing, daemon=True).start()


    while True:
        clientSocket, addr = serverSocket.accept()
        print(f"Połączono z {addr}")

        # Uruchamiamy nowy wątek dla każdego klienta
        threading.Thread(target=gameServer.clientHandler, args=(clientSocket,)).start()

# Uruchomienie serwera
if __name__ == "__main__":
    startServer()
