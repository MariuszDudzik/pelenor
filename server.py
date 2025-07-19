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
        self.next_session_id = 1             # ID do śledzenia unikalnych sesji
        self.lock = threading.Lock()       # Lock do synchronizacji dostępu do sesji
        self.msg_f_client = server_data_handler.MsgFClient()
   
  
    def _send_json(self, client_socket, data):
        if not isinstance(data, dict):
            return
        json_string = json.dumps(data)  
        request_bytes = json_string.encode('utf-8')  
        request_length = len(request_bytes)
        client_socket.sendall(struct.pack('!I', request_length))
        client_socket.sendall(request_bytes)


    def client_handler(self, client_socket):
        try:
            while True:
                length_data = b""
                while len(length_data) < 4:
                    packet = client_socket.recv(4 - len(length_data))
                    if not packet:
                        return
                    length_data += packet

                response_length = struct.unpack('!I', length_data)[0]
                received_data = b""
                while len(received_data) < response_length:
                    packet = client_socket.recv(min(4096, response_length - len(received_data)))
                    if not packet:
                        raise ConnectionError("Połączenie zerwane w trakcie odbierania danych.")
                    received_data += packet

                data = json.loads(received_data.decode())
                self.handle_action(client_socket, data)

        except Exception as e:
            print(f"Błąd odbioru danych: {e}")
            

    def handle_action(self, client_socket, data):
        action = data.get('action')
        match action:
            case 'create_game':
                with self.lock:
                    session_id = self.next_session_id
                    server_con = servercontroller.ServerController()
                    player_, board_ = self.msg_f_client.create_game(client_socket, data, server_con)
                    self.sessions[session_id] = {'players': [player_], 'arena': board_, 'handler': server_con}
                    self.next_session_id += 1
                    print(f"Sesja {session_id} utworzona przez {player_.login}.")
                    sessions = self.msg_f_client.open_sessions_game(self.sessions)
                    self._send_json(client_socket, {'action': 'game_created', 'session_id': session_id, 'sessions': sessions})
            case 'list_sessions':
                with self.lock:
                    sessions = self.msg_f_client.open_sessions_game(self.sessions)
                    self._send_json(client_socket, {'action': 'list_sessions', 'sessions': sessions})
            case 'join_game':
                with self.lock:
                    session_id = data.get('session_id')
                    if session_id not in self.sessions:
                        self._send_json(client_socket, {'action': 'joined_game', 'error': 'Session not found'})
                    elif self.msg_f_client.is_full(self.sessions, session_id):
                        self._send_json(client_socket, {'action': 'joined_game', 'error': 'Session is full'})
                    else:
                        player_ = self.msg_f_client.prepare_second_player(client_socket, data, self.sessions)
                        self.sessions[session_id]['players'].append(player_)
                        gamelogic.GameLogic.s_deploy_palace_gward(self.sessions[session_id]['arena'], self.sessions[session_id]['players'])
                        print(f"Gracz {player_.login} dołączył do sesji {session_id}.")
                        self._send_json(client_socket, {'action': 'joined_game', 'session_id': session_id})
                        parcel = self.msg_f_client.start_game(self.sessions[session_id]['players'],
                                                               self.sessions[session_id]['arena'])
                        for player in self.sessions[session_id]['players']:
                            self._send_json(player.socket, {'action': 'start_game', 'data': parcel})
            case 'deploy':
                with self.lock:
                    session_id = data.get('session_id')
                    if session_id in self.sessions:
                        parcel = self.msg_f_client.deploy_unit(self.sessions[session_id], data)
                        for player in self.sessions[session_id]['players']:
                            self._send_json(player.socket, {'action': 'deploy', 'data': parcel})

            case 'ping':
                with self.lock:
                    session_id = data.get('session_id')
                    if session_id != None:
                        try:
                            for player in self.sessions[session_id]['players']:
                                if player.socket == client_socket:
                                    player.last_ping_time = time.time()
                        except:
                            print(f"Brak sesji {session_id}")
            case _:
                print(f"Nieznana akcja: {action}")
                    

    def player_last_ping(self):
        while True:
            with self.lock:
                for session_id, session_data in list(self.sessions.items()):
                    for player in list(session_data['players']):
                        if time.time() - player.last_ping_time > 30:
                            print(f"Gracz {player.login} nie odpowiada. Usuwam go z sesji {session_id}")
                            session_data['players'].remove(player)

                    if len(session_data['players']) == 0:
                        del self.sessions[session_id]
                        print(f"Sesja {session_id} została automatycznie usunięta (brak graczy).")
            time.sleep(5)


def start_server():
    game_server = GameServer()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 25565))
    server_socket.listen(100)
    print("Serwer oczekuje na połączenia...")
    threading.Thread(target=game_server.player_last_ping, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Połączono z {addr}")
        threading.Thread(target=game_server.client_handler, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
