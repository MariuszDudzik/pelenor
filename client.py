import socket
import json
import time
import message_from_server
import message_to_server
import threading
import select
import struct

class Client(object):
    def __init__(self, gameController, game, eventbus):
        self.clientSocket = None
        self.serverAddress = None
        self.port = None
        self.action = None
        self.connectionStatus = ""
        self.tping = None
        self.treceive = None
        self.stop_event = threading.Event()
        self.messageFromServer = message_from_server.MessageFromServer(gameController, game, eventbus)
        self.messageToServer = message_to_server.MessageToServer(gameController, game)

        self._loadServerAddress()


    def _stopThreads(self):
        self.stop_event.set()
        if self.tping and self.tping.is_alive():
            self.tping.join()
        if self.treceive and self.treceive.is_alive():
            self.treceive.join()
 

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
            self.tping = threading.Thread(target=self.pingServer, daemon=True)
            self.treceive = threading.Thread(target=self.receiveData, daemon=True)
            self.tping.start()
            self.treceive.start()
        except Exception as e:
            self.setConnectionStatus(f"Błąd połączenia: {e}")
            self.setSocket(None)


    def getsocket(self):
        return self.clientSocket
    

    def setSocket(self, nowSocket):
        self.clientSocket = nowSocket
    

    def close_connection(self):
        self._stopThreads()
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
        while not self.stop_event.is_set():
            try:
                self.messageToServer.ping(self.getsocket())
                for _ in range(70):
                    if self.stop_event.is_set():
                        return
                    time.sleep(0.2)
            except (socket.error, json.JSONDecodeError) as e:
                print(f"Błąd podczas pingowania: {e}")
                return


    def receiveData(self):
        while not self.stop_event.is_set():
            try:
                ready, _, _ = select.select([self.clientSocket], [], [], 0.2)
                if not ready:
                    continue
                length_data = b""
                while len(length_data) < 4:
                    packet = self.clientSocket.recv(4 - len(length_data))
                    if not packet:
                        return
                    length_data += packet

                response_length = struct.unpack('!I', length_data)[0]

                received_data = b""
                while len(received_data) < response_length:
                    packet = self.clientSocket.recv(min(4096, response_length - len(received_data)))
                    if not packet:
                        raise ConnectionError("Połączenie zerwane w trakcie odbierania danych.")
                    received_data += packet

                data = json.loads(received_data.decode())
                self.messageFromServer.serverResponseHandle(data)

            except Exception as e:
                print(f"Błąd odbioru danych: {e}")
                return


    def gameClient(self):
        action = self.getAction()   
        if action:
            match action:
                case 'create_game':
                    self.messageToServer.createGame(self.getsocket())
                case 'list_sessions':
                    self.messageToServer.listSessions(self.getsocket())
                case 'join_game':
                    self.messageToServer.joinGame(self.getsocket())


