import socket
import json
import time
import msgFserver
import msgTServer
import threading
import select
import struct

class Client(object):
    def __init__(self, game_controller, game, eventbus):
        self.client_socket = None
        self.server_address = None
        self.port = None
        self.action = None
        self.connection_status = ""
        self.tping = None
        self.treceive = None
        self.stop_event = threading.Event()
        self.msg_f_server = msgFserver.MsgFServer(game_controller, game, eventbus)
        self.msg_t_server = msgTServer.MsgTServer(game_controller, game)
        self.play = None

        self._load_server_address()


    def set_play(self, play):
        self.play = play
        self.msg_f_server.set_play(play)


    def _stop_threads(self):
        self.stop_event.set()
        if self.tping and self.tping.is_alive():
            self.tping.join()
        if self.treceive and self.treceive.is_alive():
            self.treceive.join()
 

    def _load_server_address(self):
        with open("server.dat", "r") as file:
            self.server_address = file.readline().strip()
            self.port = int(file.readline().strip())


    def start_connection(self):
        server_address = (self.server_address, self.port)
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(server_address)
            self.set_connection_status("Połączono z serwerem")
            self.tping = threading.Thread(target=self.ping_server, daemon=True)
            self.treceive = threading.Thread(target=self.receive_data, daemon=True)
            self.tping.start()
            self.treceive.start()
        except Exception as e:
            self.set_connection_status(f"Błąd połączenia: {e}")
            self.set_socket(None)


    def get_socket(self):
        return self.client_socket

    def set_socket(self, now_socket):
        self.client_socket = now_socket


    def close_connection(self):
        self._stop_threads()
        if self.client_socket:
            try:
                self.client_socket.close()
            except OSError:
                pass 
            finally:
                self.set_socket(None)


    def get_action(self):
        return self.action
    

    def set_action(self, action):
        self.action = action

    def get_connection_status(self):
        return self.connection_status

    def set_connection_status(self, connection_status):
        self.connection_status = connection_status


    def ping_server(self):
        while not self.stop_event.is_set():
            try:
                self.msg_t_server.ping(self.get_socket())
                for _ in range(70):
                    if self.stop_event.is_set():
                        return
                    time.sleep(0.2)
            except (socket.error, json.JSONDecodeError) as e:
                print(f"Błąd podczas pingowania: {e}")
                return


    def receive_data(self):
        while not self.stop_event.is_set():
            try:
                ready, _, _ = select.select([self.client_socket], [], [], 0.2)
                if not ready:
                    continue
                length_data = b""
                while len(length_data) < 4:
                    packet = self.client_socket.recv(4 - len(length_data))
                    if not packet:
                        return
                    length_data += packet

                response_length = struct.unpack('!I', length_data)[0]

                received_data = b""
                while len(received_data) < response_length:
                    packet = self.client_socket.recv(min(4096, response_length - len(received_data)))
                    if not packet:
                        raise ConnectionError("Połączenie zerwane w trakcie odbierania danych.")
                    received_data += packet

                data = json.loads(received_data.decode())
                self.msg_f_server.server_response_handle(data)

            except Exception as e:
                print(f"Błąd odbioru danych: {e}")
                return


    def game_client(self):
        action = self.get_action()
        if action:
            match action:
                case 'create_game':
                    self.msg_t_server.create_game(self.get_socket())
                case 'list_sessions':
                    self.msg_t_server.list_sessions(self.get_socket())
                case 'join_game':
                    self.msg_t_server.join_game(self.get_socket())


